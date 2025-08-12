# 🏔️ Visualizador 3D de Horizonte - Ecuador

Una aplicación de visualización 3D interactiva que permite explorar el terreno y el horizonte geográfico del Ecuador continental utilizando datos de elevación SRTM.

## 📋 Descripción General

Este proyecto proporciona una herramienta profesional para visualizar el terreno en 3D, permitiendo a los usuarios:
- Explorar cualquier ubicación dentro del Ecuador continental
- Visualizar el horizonte geográfico desde cualquier punto de observación
- Analizar el perfil del terreno en tiempo real
- Interactuar con modelos 3D precisos basados en datos reales de elevación

## 🚀 Características Principales

- **Visualización 3D Interactiva**: Modelado tridimensional preciso del terreno
- **Datos SRTM**: Utiliza archivos .hgt de alta resolución (90m)
- **Interfaz Gráfica Intuitiva**: Interfaz PyQt5 amigable para usuarios
- **Ubicaciones Preconfiguradas**: 14 ubicaciones importantes del Ecuador
- **Rendimiento Optimizado**: Submuestreo inteligente para mantener fluidez
- **Precisión Geográfica**: Coordenadas exactas y elevaciones reales

## 🗺️ Cobertura Geográfica

El proyecto cubre todo el territorio continental del Ecuador:
- **Latitud**: -5° a 2°
- **Longitud**: -82° a -75°
- **Resolución**: 90 metros por píxel (datos SRTM)

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **PyQt5**: Interfaz gráfica de usuario
- **NumPy**: Procesamiento numérico y matrices
- **PyVista**: Visualización 3D y renderizado
- **VTK**: Motor de renderizado 3D
- **SRTM Data**: Datos de elevación del Shuttle Radar Topography Mission

## 📁 Estructura del Proyecto

```
Proyecto_IIB/
├── main.py                 # Punto de entrada principal
├── config.py              # Configuración global
├── requirements.txt       # Dependencias del proyecto
├── data/                  # Archivos .hgt de elevación
│   ├── N00W073.hgt
│   ├── N00W074.hgt
│   └── ...
├── core/                  # Módulos principales
│   ├── terrain_data.py    # Carga de datos de terreno
│   └── viewer_3d.py       # Visualización 3D
├── gui/                   # Interfaz gráfica
│   └── main_window.py     # Ventana principal
└── assets/                # Recursos gráficos (si existen)
```

## 🎯 Casos de Uso

- **Turismo**: Planificación de rutas y visualización de destinos
- **Educación**: Enseñanza de geografía y topografía
- **Arquitectura**: Análisis de sitios para construcción
- **Agricultura**: Estudio de terrenos para cultivos
- **Investigación**: Análisis geoespacial y ambiental

## 🏗️ Desarrollo

Este proyecto fue desarrollado como parte del curso de Ingeniería Informática Básica (IIB) - Grupo 3, utilizando metodologías de desarrollo ágil y buenas prácticas de programación.

## 📄 Documentación Adicional

- [Manual de Uso](MANUAL_DE_USO.md) - Guía completa de instalación y uso
- [Informe Final](InformeFinal_IIB_Grupo3.pdf) - Documentación técnica detallada

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abra un issue o envíe un pull request para mejoras.

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y no comercial.

---

**Desarrollado con ❤️ por el Grupo 3 - IIB**
