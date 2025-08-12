"""
Módulo para la visualización avanzada del terreno utilizando PyVista.
"""

import numpy as np
import math
import pyvista as pv
from core.terrain_data import TerrainDataLoader
from config import (
    DEFAULT_VIEW_RADIUS_KM, DEFAULT_FIELD_OF_VIEW, OBSERVER_HEIGHT_M,
    MAX_RENDER_POINTS, TERRAIN_CMAP, BACKGROUND_COLOR
)

class Horizon3DViewer:
    """
    Clase para generar y mostrar vistas realistas y mejoradas del horizonte.
    """
    def __init__(self, terrain_data_loader: TerrainDataLoader):
        self.terrain_loader = terrain_data_loader
        self.plotter = None
        self.current_camera_position = [0, 0, 0]
        self.current_focal_point = [0, 0, 0]
        self.current_azimut = DEFAULT_FIELD_OF_VIEW
        self.current_field_of_view = DEFAULT_FIELD_OF_VIEW
        self.observer_terrain_height = 0
        self.observer_total_height = 0
        self.inverted_view = False

    def _invert_view(self):
        """Invierte la visualización rotando la cámara 180 grados alrededor del eje Z."""
        if self.plotter:
            # Guardar posición y orientación actual
            current_pos = np.array(self.plotter.camera.position)
            focal_point = np.array(self.plotter.camera.focal_point)
            up_vector = np.array(self.plotter.camera.up)
            
            # Calcular nueva posición (simétrico respecto al punto focal)
            new_pos = 2 * focal_point - current_pos
            new_pos[2] = current_pos[2]  # Mantener misma altura
            
            # Actualizar cámara
            self.plotter.camera.position = new_pos
            self.plotter.camera.focal_point = focal_point
            self.plotter.camera.up = up_vector * [-1, -1, 1]  # Invertir vectores X e Y
            
            self.inverted_view = not self.inverted_view
            self.plotter.render()

    def _get_cardinal_direction(self, angle: float) -> str:
        """Convierte un ángulo en grados a una dirección cardinal."""
        dirs = ["Norte", "Noreste", "Este", "Sureste", "Sur", "Suroeste", "Oeste", "Noroeste"]
        idx = int(((angle % 360) + 22.5) // 45) % 8
        return dirs[idx]

    def generate_3d_view(self, lat_observer: float, lon_observer: float, 
                         azimut: int = 90, field_of_view: int = 90, 
                         view_radius_km: int = 150, location_name: str = "Ubicación Personalizada") -> dict:
        """
        Genera una vista mejorada del terreno centrada en el observador.
        
        Args:
            lat_observer: Latitud del observador en grados decimales
            lon_observer: Longitud del observador en grados decimales
            azimut: Dirección de la vista en grados (0=Norte, 90=Este)
            field_of_view: Ángulo de visión en grados (10-120)
            view_radius_km: Radio de visualización en kilómetros
            location_name: Nombre descriptivo de la ubicación
            
        Returns:
            dict: Diccionario con información de la vista generada
        """
        print(f"Generando vista para: ({lat_observer:.6f}°, {lon_observer:.6f}°)")
        print(f"Azimut: {azimut}° | FOV: {field_of_view}° | Radio: {view_radius_km}km")

        if self.terrain_loader.full_terrain_matrix is None:
            raise RuntimeError("La matriz de terreno no ha sido cargada antes de generar la vista.")

        # Convertir coordenadas a índices de matriz
        obs_row, obs_col = self.terrain_loader.coords_to_indices(lat_observer, lon_observer)
        self.observer_terrain_height = self.terrain_loader.full_terrain_matrix[obs_row, obs_col]
        
        # Manejar datos faltantes de elevación
        if self.observer_terrain_height == -32768:
            self.observer_terrain_height = 0
            print("Advertencia: No hay datos de elevación en la posición del observador. Usando 0m.")
        
        self.observer_total_height = self.observer_terrain_height + OBSERVER_HEIGHT_M

        # Calcular región de interés alrededor del observador
        approx_meters_per_degree = 111000
        meters_per_index = approx_meters_per_degree / (self.terrain_loader.hgt_resolution - 1)
        radius_indices = int((view_radius_km * 1000) / meters_per_index)

        row_min = max(0, obs_row - radius_indices)
        row_max = min(self.terrain_loader.full_terrain_matrix.shape[0], obs_row + radius_indices)
        col_min = max(0, obs_col - radius_indices)
        col_max = min(self.terrain_loader.full_terrain_matrix.shape[1], obs_col + radius_indices)

        # Reducir densidad de puntos para mejor rendimiento
        step = max(1, int(radius_indices / MAX_RENDER_POINTS))
        terrain_region = self.terrain_loader.full_terrain_matrix[row_min:row_max:step, col_min:col_max:step]

        if terrain_region.size == 0:
            raise ValueError("La región del terreno está vacía. Ajuste las coordenadas o el radio.")

        # Procesamiento de datos de elevación
        terrain_region = terrain_region.astype(float)
        terrain_region[terrain_region == -32768] = 0.0

        # Crear malla de coordenadas
        rows, cols = terrain_region.shape
        x_coords = np.arange(cols) * meters_per_index * step / 1000  # Convertir a km
        y_coords = np.arange(rows) * meters_per_index * step / 1000

        # Centrar coordenadas en el observador
        obs_x_relative = (obs_col - col_min) * meters_per_index * step / 1000
        obs_y_relative = (obs_row - row_min) * meters_per_index * step / 1000
        x_coords -= obs_x_relative
        y_coords -= obs_y_relative

        # Crear superficie
        Z_elevations_km = terrain_region / 1000.0  # Convertir a km
        X, Y = np.meshgrid(x_coords, y_coords)
        surface = pv.StructuredGrid(X, Y, Z_elevations_km)

        # Normalización de elevaciones para coloreado
        elevations_m = surface.points[:, 2] * 1000
        min_elev_data = np.min(elevations_m)
        max_elev_data = np.max(elevations_m)
        elev_range = max(max_elev_data - min_elev_data, 1)
        normalized_elevations = (elevations_m - min_elev_data) / elev_range
        surface["elevacion_normalizada"] = normalized_elevations

        # Configurar plotter
        if self.plotter is not None:
            self.plotter.close()
            self.plotter = None

        self.plotter = pv.Plotter(window_size=[1400, 900])
        self.plotter.set_background(BACKGROUND_COLOR)
        
        # Habilitar efectos visuales avanzados
        self.plotter.enable_eye_dome_lighting()
        self.plotter.enable_depth_peeling()
        self.plotter.renderer.SetUseDepthPeeling(True)
        self.plotter.renderer.SetMaximumNumberOfPeels(8)
        self.plotter.renderer.SetOcclusionRatio(0.05)

        # Añadir terreno con sombreado realista
        self.plotter.add_mesh(
            surface,
            scalars="elevacion_normalizada",
            cmap=TERRAIN_CMAP,
            smooth_shading=True,
            show_edges=False,
            metallic=0.3,
            roughness=0.7,
            ambient=0.4,
            diffuse=0.8,
            specular=0.1,
            clim=[0.0, 1.0],
            show_scalar_bar=False,
            lighting=True,
            opacity=1.0
        )

        # Añadir wireframe sutil
        self.plotter.add_mesh(
            surface,
            color="#444444",
            style="wireframe",
            opacity=0.1,
            line_width=0.8
        )

        # Configuración avanzada de la cámara (CORREGIDA)
        self.current_azimut = azimut
        self.current_field_of_view = field_of_view
        camera_height_km = self.observer_total_height / 1000.0
        azimut_rad = math.radians(azimut)
        
        # Posición de la cámara (detrás y arriba del observador)
        camera_distance_km = view_radius_km * 0.4
        cam_x = -camera_distance_km * math.sin(azimut_rad)  # Negativo para posición detrás
        cam_y = -camera_distance_km * math.cos(azimut_rad)
        cam_z = camera_height_km + 0.1  # Levantamos un poco la cámara
        
        # Punto focal (delante del observador)
        focal_distance_km = view_radius_km * 0.1
        focal_x = focal_distance_km * math.sin(azimut_rad)
        focal_y = focal_distance_km * math.cos(azimut_rad)
        focal_z = camera_height_km * 0.9  # Mirar ligeramente hacia abajo
        
        # Configurar cámara
        self.current_camera_position = [cam_x, cam_y, cam_z]
        self.current_focal_point = [focal_x, focal_y, focal_z]
        
        self.plotter.camera.position = self.current_camera_position
        self.plotter.camera.focal_point = self.current_focal_point
        self.plotter.camera.up = [0, 0, 1]  # Eje Z como arriba
        self.plotter.camera.view_angle = field_of_view

        # Configurar rangos de clipping
        near_clip = 0.001
        far_clip = view_radius_km * 2.5
        self.plotter.camera.clipping_range = (near_clip, far_clip)

        # Configurar interacción
        self.plotter.track_mouse_position = True
        self.plotter.enable_trackball_style()  # Rotación libre con mouse
        
        # Teclas especiales
        self.plotter.add_key_event('space', self._invert_view)
        self.plotter.add_key_event('q', self.plotter.close)

        # Añadir información de ubicación
        text = f"{location_name}\nLat: {lat_observer:.6f}°\nLon: {lon_observer:.6f}°"
        self.plotter.add_text(text, position='upper_left', font_size=14, color='white', shadow=True)

        # Información de retorno
        info_data = {
            'plotter': self.plotter,
            'azimut_actual': self.current_azimut,
            'field_of_view_actual': self.current_field_of_view,
            'observer_height_m': self.observer_total_height,
            'terrain_height_m': self.observer_terrain_height,
            'cardinal_direction': self._get_cardinal_direction(azimut),
            'coordinates': (lat_observer, lon_observer),
            'view_radius_km': view_radius_km,
            'max_elevation_m': max_elev_data,
            'min_elevation_m': min_elev_data,
            'rendered_points': surface.n_points,
            'location_name': location_name
        }
        
        return info_data

    def show_view(self):
        """Muestra la ventana de visualización con todas las interacciones."""
        if self.plotter:
            # Configuración final antes de mostrar
            self.plotter.enable_anti_aliasing('ssaa')
            self.plotter.show(auto_close=False)
        else:
            print("Error: No hay vista para mostrar. Genere una vista primero.")

    def update_camera_direction(self, new_azimut: int):
        """Actualiza la dirección de la cámara en la vista."""
        if self.plotter:
            self.current_azimut = new_azimut
            azimut_rad = math.radians(new_azimut)
            
            # Actualizar posición y punto focal manteniendo las distancias
            cam_dist = np.linalg.norm(self.current_camera_position)
            focal_dist = np.linalg.norm(self.current_focal_point)
            
            self.plotter.camera.position = [
                -cam_dist * math.sin(azimut_rad),
                -cam_dist * math.cos(azimut_rad),
                self.current_camera_position[2]
            ]
            
            self.plotter.camera.focal_point = [
                focal_dist * math.sin(azimut_rad),
                focal_dist * math.cos(azimut_rad),
                self.current_focal_point[2]
            ]
            
            self.plotter.camera.up = [0, 0, 1]
            self.plotter.render()

    def update_camera_zoom(self, new_field_of_view: int):
        """Actualiza el zoom (campo de visión) de la cámara."""
        if self.plotter:
            self.current_field_of_view = max(10, min(120, new_field_of_view))
            self.plotter.camera.view_angle = self.current_field_of_view
            self.plotter.render()