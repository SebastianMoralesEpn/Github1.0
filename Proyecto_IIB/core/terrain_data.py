# core/terrain_data.py
"""
Módulo para la carga y gestión de datos de elevación del terreno (.hgt).
"""

import math
import numpy as np
from pathlib import Path
from config import DATA_DIR, HGT_RESOLUTION

from PyQt5.QtCore import QObject, pyqtSignal

class TerrainDataLoader(QObject):
    """
    Carga y gestiona datos de elevación del terreno a partir de archivos .hgt.
    """

    # Señales para comunicación con la GUI
    full_terrain_matrix_loaded = pyqtSignal()
    error_loading_matrix = pyqtSignal(str)

    def __init__(self, data_directory: str = DATA_DIR):
        super().__init__()
        self.data_directory = Path(data_directory)
        self.hgt_resolution = HGT_RESOLUTION
        self.full_terrain_matrix = None
        self.available_hgt_files = {}
        self.sorted_lats = []
        self.sorted_lons = []
        self.lat_min_matrix = None
        self.lat_max_matrix = None
        self.lon_min_matrix = None
        self.lon_max_matrix = None

        try:
            self._scan_available_hgt_files()
        except Exception as e:
            self.error_loading_matrix.emit(f"Error al escanear archivos HGT: {e}")

    # --- Métodos privados ---

    def _generate_hgt_filename(self, lat: float, lon: float) -> str:
        """Genera el nombre de archivo .hgt para una coordenada dada."""
        lat_label = 'N' if lat >= 0 else 'S'
        lon_label = 'E' if lon >= 0 else 'W'
        return f"{lat_label}{abs(int(lat)):02d}{lon_label}{abs(int(lon)):03d}.hgt"

    def _scan_available_hgt_files(self):
        """
        Escanea el directorio de datos para identificar los archivos .hgt disponibles.
        """
        print(f"Escaneando archivos .hgt en: {self.data_directory}")
        found_lats, found_lons = set(), set()
        scan_lat_min, scan_lat_max = -8, 3
        scan_lon_min, scan_lon_max = -82, -73

        for lat_int in range(scan_lat_min, scan_lat_max + 1):
            for lon_int in range(scan_lon_min, scan_lon_max + 1):
                filename = self._generate_hgt_filename(lat_int, lon_int)
                filepath = self.data_directory / filename
                if filepath.is_file():
                    self.available_hgt_files[(lat_int, lon_int)] = filepath
                    found_lats.add(lat_int)
                    found_lons.add(lon_int)

        if not found_lats or not found_lons:
            raise FileNotFoundError("No se encontraron archivos .hgt válidos en el directorio.")

        self.sorted_lats = sorted(found_lats, reverse=True)
        self.sorted_lons = sorted(found_lons)
        self.lat_min_matrix = min(self.sorted_lats)
        self.lat_max_matrix = max(self.sorted_lats)
        self.lon_min_matrix = min(self.sorted_lons)
        self.lon_max_matrix = max(self.sorted_lons)

        print(f"Archivos .hgt encontrados: {len(self.available_hgt_files)}")
        print(f"Rango de datos disponible: Lat {self.lat_min_matrix}° a {self.lat_max_matrix}°, Lon {self.lon_min_matrix}° a {self.lon_max_matrix}°")

    def _load_single_hgt(self, filepath: Path) -> np.ndarray:
        """Carga un archivo .hgt y devuelve su matriz de elevación."""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            matrix = np.frombuffer(data, dtype='>i2').reshape((self.hgt_resolution, self.hgt_resolution))
            return matrix
        except Exception as e:
            print(f"Error al cargar {filepath}: {e}")
            return np.full((self.hgt_resolution, self.hgt_resolution), -32768, dtype=np.int16)

    # --- Métodos públicos ---

    def load_full_terrain_matrix(self):
        """
        Ensambla todos los archivos .hgt en una única matriz de terreno.
        """
        if self.full_terrain_matrix is not None:
            print("Matriz de terreno ya cargada.")
            self.full_terrain_matrix_loaded.emit()
            return self.full_terrain_matrix

        print("Ensamblando matriz de terreno completa...")
        try:
            rows_of_blocks = []
            for i, lat_int in enumerate(self.sorted_lats):
                current_row_blocks = []
                for j, lon_int in enumerate(self.sorted_lons):
                    filepath = self.available_hgt_files.get((lat_int, lon_int))
                    block = self._load_single_hgt(filepath) if filepath else np.full((self.hgt_resolution, self.hgt_resolution), -32768, dtype=np.int16)
                    # Recortar bordes compartidos
                    if j < len(self.sorted_lons) - 1:
                        block = block[:, :-1]
                    if i < len(self.sorted_lats) - 1:
                        block = block[:-1, :]
                    current_row_blocks.append(block)
                if current_row_blocks:
                    rows_of_blocks.append(np.hstack(current_row_blocks))
            if rows_of_blocks:
                self.full_terrain_matrix = np.vstack(rows_of_blocks)
                print(f"Matriz de terreno completa cargada: {self.full_terrain_matrix.shape}")
                self.full_terrain_matrix_loaded.emit()
            else:
                raise ValueError("No se pudo ensamblar la matriz de terreno.")
            return self.full_terrain_matrix
        except Exception as e:
            self.error_loading_matrix.emit(f"Error al cargar la matriz de terreno: {e}")
            self.full_terrain_matrix = None
            return None

    def coords_to_indices(self, lat: float, lon: float) -> tuple[int, int]:
        """
        Convierte coordenadas (lat, lon) a índices (row, col) en la matriz de terreno.
        """
        if self.full_terrain_matrix is None:
            raise RuntimeError("La matriz de terreno no ha sido cargada.")

        if not (self.lat_min_matrix <= lat < self.lat_max_matrix + 1 and
                self.lon_min_matrix <= lon < self.lon_max_matrix + 1):
            raise ValueError(f"Coordenadas ({lat}, {lon}) fuera del rango de datos disponibles.")

        lat_block_origin = int(math.floor(lat)) if lat >= 0 else int(math.ceil(lat))
        lon_block_origin = int(math.floor(lon)) if lon >= 0 else int(math.ceil(lon))
        lat_block_idx = self.sorted_lats.index(lat_block_origin)
        lon_block_idx = self.sorted_lons.index(lon_block_origin)

        relative_lat = lat - lat_block_origin
        if lat_block_origin < 0:
            relative_lat = 1 - (lat - lat_block_origin)
        relative_lon = lon - lon_block_origin

        rows_in_block = self.hgt_resolution - (1 if lat_block_idx < len(self.sorted_lats) - 1 else 0)
        cols_in_block = self.hgt_resolution - (1 if lon_block_idx < len(self.sorted_lons) - 1 else 0)
        row_in_block = int(relative_lat * (rows_in_block - 1))
        col_in_block = int(relative_lon * (cols_in_block - 1))
        row_in_block = max(0, min(row_in_block, rows_in_block - 1))
        col_in_block = max(0, min(col_in_block, cols_in_block - 1))

        global_row = sum(self.hgt_resolution - (1 if i < len(self.sorted_lats) - 1 else 0) for i in range(lat_block_idx)) + row_in_block
        global_col = sum(self.hgt_resolution - (1 if j < len(self.sorted_lons) - 1 else 0) for j in range(lon_block_idx)) + col_in_block
        global_row = max(0, min(global_row, self.full_terrain_matrix.shape[0] - 1))
        global_col = max(0, min(global_col, self.full_terrain_matrix.shape[1] - 1))

        return global_row, global_col

    def get_elevation_at_coords(self, lat: float, lon: float) -> float:
        """
        Obtiene la elevación en metros para una latitud y longitud dadas.
        """
        if self.full_terrain_matrix is None:
            raise RuntimeError("La matriz de terreno no ha sido cargada.")
        row, col = self.coords_to_indices(lat, lon)
        elevation = self.full_terrain_matrix[row, col]
        return 0.0 if elevation == -32768 else float(elevation)
