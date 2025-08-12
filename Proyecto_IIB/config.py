# config.py
"""
Configuración global para el Visualizador del Horizonte - Ecuador.
Define constantes y parámetros clave para la aplicación.
"""

import os

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Parámetros del Terreno
HGT_RESOLUTION = 1201  # Puntos por grado en archivos .hgt
EQUATOR_LAT_RANGE = (-5, 2) # Rango aproximado de latitud para Ecuador continental
EQUATOR_LON_RANGE = (-82, -75) # Rango aproximado de longitud para Ecuador continental

# Parámetros de Visualización 
DEFAULT_VIEW_RADIUS_KM = 75 # Radio por defecto para la visualización del terreno
DEFAULT_FIELD_OF_VIEW = 90   # Campo de visión por defecto en grados
OBSERVER_HEIGHT_M = 0.5      # Altura estándar del observador sobre el terreno en metros
MAX_RENDER_POINTS = 2000     # Máximo de puntos para submuestreo del terreno para rendimiento

# Colores y Estilos (PyVista)
TERRAIN_CMAP = "terrain"  # Mapa de colores para el terreno
TERRAIN_COLOR = "tan"      # Color base del terreno
SKY_COLOR = "skyblue"      # Color del cielo
GROUND_COLOR = "saddlebrown" # Color del suelo
BACKGROUND_COLOR = "lightblue" # Color de fondo de la ventana

# Ubicaciones Preconfiguradas
PRESET_LOCATIONS = {
    "🏔️ Quito - Capital Andina": (-0.1807, -78.4678),
    "🏖️ Guayaquil - Puerto Principal": (-2.1709, -79.9224),
    "🏛️ Cuenca - Ciudad Patrimonio": (-2.9001, -79.0059),
    "⚓ Manta - Costa del Pacífico": (-0.9673, -80.2627),
    "🌴 Esmeraldas - Zona Norte": (0.9538, -79.6528),
    "🎵 Loja - Tierra de la Música": (-3.9890, -79.2036),
    "🌋 Ambato - Corazón del Ecuador": (-1.2549, -78.6291),
    "⛰️ Riobamba - Sierra Central": [-1.6735, -78.6483],
    "🏞️ Ibarra - Lagos Andinos": [0.3517, -78.1222],
    "🚢 Machala - Puerto Internacional": [-3.2581, -79.9554],
    "🗻 Volcán Cotopaxi": (-0.6137, -78.4729),
    "🏔️ Chimborazo - Cumbre más alta": (-1.4691, -78.8175),
    "🌊 Playas - Costa ecuatoriana": (-2.2028, -80.3844),
    "🌉 Cotopaxi": (-0.5813275, -78.4314093)
}

# Mensajes de Usuario
MSG_LOADING_TERRAIN = "Cargando datos de elevación..."
MSG_GENERATING_VIEW = "Generando vista"
MSG_READY = "Listo para generar la vista"
MSG_ERROR_COORDS = "Coordenadas inválidas. Verifique los rangos para Ecuador."
MSG_ERROR_NO_DATA = "No hay datos de elevación para la ubicación seleccionada."
MSG_ERROR_PYVISTA = "PyVista no está instalado o configurado correctamente."
