# 📖 Manual de Uso - Visualizador 3D de Horizonte - Ecuador

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python 3.8 o superior**
- **Sistema operativo**: Windows 10/11, macOS o Linux
- **Memoria RAM**: Mínimo 4GB (8GB recomendado)
- **Espacio en disco**: 500MB para datos de elevación

### Paso 1: Instalación de Dependencias

1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/SebastianMoralesEpn/Github1.0/tree/0da0d9adbc6e6961cc6165a288c41a55de2f75c9/Proyecto_IIB]
   cd Proyecto_IIB
   ```

2. **Crear entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

### Paso 2: Verificación de Datos

Asegúrese de que la carpeta `data/` contenga los archivos `.hgt` necesarios:
- Los archivos deben tener el formato: `NXXWXXX.hgt` o `SXXWXXX.hgt`
- Cada archivo debe tener exactamente 2.8MB de tamaño
- Debe haber al menos un archivo para la región que desea visualizar

## 🎯 Uso Básico

### Iniciar la Aplicación

1. **Desde la terminal**:
   ```bash
   python main.py
   ```

2. **La ventana principal se abrirá** mostrando:
   - Panel de control izquierdo
   - Área de visualización 3D
   - Barra de menú superior

### Interfaz de Usuario

#### Panel de Control (Izquierda)
- **Coordenadas**: Ingrese latitud y longitud manualmente
- **Ubicaciones Preconfiguradas**: Seleccione de 14 ubicaciones importantes
- **Parámetros de Visualización**:
  - Radio de visualización (km)
  - Campo de visión (grados)
  - Altura del observador (m)

#### Controles 3D
- **Rotación**: Click izquierdo + arrastrar
- **Zoom**: Rueda del mouse
- **Pan**: Click derecho + arrastrar
- **Reset**: Barra espaciadora

## 📍 Ubicaciones Preconfiguradas

| Ubicación | Coordenadas | Descripción |
|-----------|-------------|-------------|
| **Quito** | -0.1807, -78.4678 | Capital andina a 2850m |
| **Guayaquil** | -2.1709, -79.9224 | Puerto principal |
| **Cuenca** | -2.9001, -79.0059 | Ciudad patrimonio |
| **Manta** | -0.9673, -80.2627 | Costa del Pacífico |
| **Esmeraldas** | 0.9538, -79.6528 | Zona norte tropical |
| **Loja** | -3.9890, -79.2036 | Tierra de la música |
| **Ambato** | -1.2549, -78.6291 | Corazón del Ecuador |
| **Riobamba** | -1.6735, -78.6483 | Sierra central |
| **Ibarra** | 0.3517, -78.1222 | Lagos andinos |
| **Machala** | -3.2581, -79.9554 | Puerto internacional |
| **Cotopaxi** | -0.6137, -78.4729 | Volcán activo |
| **Chimborazo** | -1.4691, -78.8175 | Cumbre más alta del Ecuador |
| **Playas** | -2.2028, -80.3844 | Costa ecuatoriana |
| **Cotopaxi (Volcán)** | -0.5813275, -78.4314093 | Volcán perfecto |

## 🎮 Guía de Uso Paso a Paso

### Visualización Básica

1. **Iniciar aplicación**: Ejecute `python main.py`
2. **Seleccionar ubicación**: Use el menú desplegable de ubicaciones
3. **Ajustar parámetros**: Modifique radio y campo de visión según necesidad
4. **Generar vista**: Click en "Generar Vista 3D"
5. **Explorar**: Use controles del mouse para navegar

### Coordenadas Personalizadas

1. **Activar modo manual**: Seleccione "Coordenadas Personalizadas"
2. **Ingresar valores**:
   - **Latitud**: -5.0 a 2.0 (Sur a Norte)
   - **Longitud**: -82.0 a -75.0 (Oeste a Este)
3. **Verificar rango**: El sistema validará automáticamente
4. **Generar vista**: Click en "Aplicar y Generar"

### Ejemplos Prácticos

#### Ejemplo 1: Visualizar Quito
```
Latitud: -0.1807
Longitud: -78.4678
Radio: 50 km
Campo de visión: 90°
```

#### Ejemplo 2: Costa Ecuatoriana
```
Latitud: -2.2
Longitud: -80.4
Radio: 75 km
Campo de visión: 120°
```

## 🔧 Solución de Problemas

### Error: "La carpeta de datos no se encontró"
**Solución**:
1. Verifique que existe la carpeta `data/` en el mismo directorio que `main.py`
2. Asegúrese de que contenga archivos `.hgt` válidos
3. Verifique los permisos de lectura del directorio

### Error: "No hay datos de elevación para la ubicación"
**Solución**:
1. Verifique que las coordenadas estén dentro del rango del Ecuador (-5 a 2, -82 a -75)
2. Asegúrese de que existan archivos `.hgt` para la región solicitada
3. Use ubicaciones preconfiguradas como referencia

### Error: "PyVista no está instalado"
**Solución**:
```bash
pip install pyvista vtk
```

### Rendimiento Lento
**Solución**:
1. Reduzca el radio de visualización
2. Disminuya el campo de visión
3. Cierre otras aplicaciones pesadas
4. Verifique que tiene suficiente RAM disponible

## 📊 Parámetros de Visualización

| Parámetro | Rango | Descripción | Recomendación |
|-----------|--------|-------------|---------------|
| **Radio** | 10-200 km | Área de visualización | 50-75 km |
| **Campo de visión** | 30-180° | Ángulo de visión | 90-120° |
| **Altura observador** | 0.1-10 m | Altura del punto de vista | 0.5-2 m |
| **Máx. puntos render** | 500-5000 | Calidad vs rendimiento | 2000 puntos |

## 🎨 Personalización Visual

### Colores y Estilos
- **Terreno**: Mapa de colores "terrain"
- **Cielo**: Azul cielo
- **Suelo**: Marrón claro
- **Fondo**: Azul claro

### Configuración Avanzada
Para usuarios avanzados, los colores y estilos pueden modificarse en `config.py`:
```python
TERRAIN_CMAP = "terrain"
SKY_COLOR = "skyblue"
BACKGROUND_COLOR = "lightblue"
```

## 📞 Soporte y Contacto

Para reportar problemas o sugerencias:
- **Issues**: Crear un issue en el repositorio
- **Email**: [sebastian.morales02@epn.edu.ec]
- **Documentación**: Consulte el informe técnico adjunto

## 🔄 Actualizaciones

Para mantener el proyecto actualizado:
1. Verificar nuevas versiones en el repositorio
2. Actualizar dependencias: `pip install -r requirements.txt --upgrade`
3. Verificar compatibilidad de datos

---

**Última actualización**: [11/08/2025]
**Versión**: 1.0.0
