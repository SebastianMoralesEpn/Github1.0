# 🧠 Manual de Usuario: Clasificador de Puntos con Red Neuronal

Bienvenido al manual de usuario para la aplicación de clasificación de puntos utilizando un modelo de red neuronal. Esta herramienta permite evaluar coordenadas $(X₁, X₂)$ y visualizar su clasificación junto con una función solución de referencia.

## 🌐 Acceso a la Aplicación
Ejecuta el script Python proporcionado para iniciar la interfaz gráfica.

---

## 📝 Instrucciones de Uso

### 1. 🔢 Ingreso de Datos
- **📍 Coordenada X₁**:  
  Introduce un valor numérico entre **0 y 4** (ej: `1.5`).
- **📍 Coordenada X₂**:  
  Introduce un valor numérico entre **-0.3 y 1.2** (ej: `0.7`).

### 2. 🖱️ Funcionalidades Principales
| Botón                | Acción                                                                 |
|----------------------|-----------------------------------------------------------------------|
| **Evaluar Punto**    | Clasifica las coordenadas ingresadas (Clase 0 o 1) y las grafica.    |
| **Ocultar/Mostrar Función** | Alterna la visualización de la función solución $f(X₁)$.          |
| **Limpiar Gráfico**  | Elimina todos los puntos del gráfico.                                |

### 3. 📊 Visualización
- **Gráfico interactivo** que muestra:
  - **Puntos clasificados**:  
    - 🔵 **Azules**: Clase 1  
    - 🔴 **Rojos**: Clase 0  
  - **Función solución** (línea morada punteada) cuando está visible.
- **Área de mensajes**: Muestra resultados de clasificación o errores.

---

## ⚠️ Validaciones
- Los valores de $X₁$ y $X₂$ **deben ser numéricos** y estar dentro de los rangos permitidos.
- El modelo (`Blackbox.pkl`) debe estar disponible en el mismo directorio.

---

## 💡 Ejemplo Práctico
1. Ingresa los valores:  
   - $X₁$: `2.0`  
   - $X₂$: `0.4`  
2. Haz clic en **Evaluar Punto**.  
3. Resultado esperado:  
   - Mensaje: `"Punto evaluado: (2.00, 0.40) → Clase: 1"`  
   - Punto azul en el gráfico.  

4. Explora alternando la función solución con el botón correspondiente.

---

## 🚨 Solución de Problemas
| Error/Situación                  | Solución                              |
|----------------------------------|---------------------------------------|
| "Valores no numéricos"           | Ingresa solo números (ej: 1.5, no 'abc'). |
| "$X₁$ fuera de rango (0-4)"      | Ajusta el valor al rango permitido.   |
| Gráfico no se actualiza          | Haz clic en **Evaluar Punto** tras ingresar datos. |
| Modelo no cargado                | Verifica que `Blackbox.pkl` exista en la carpeta. |

---

## 🎨 Personalización
- **Estilos visuales**: La app usa una paleta de colores profesional (azules, rojos, morados).  
- **Tamaño de ventana**: Redimensionable (mínimo 800×600 píxeles).  

---

### 📌 Notas Adicionales
- Los puntos evaluados se guardan en memoria hasta que se limpia el gráfico.  
- La función solución es:  
  $$f(X₁) = 0.10066 \cdot \frac{\sin(10.05 \cdot X₁)}{X₁} + 0.00285$$
---