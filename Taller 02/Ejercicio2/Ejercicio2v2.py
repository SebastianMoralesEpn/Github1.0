import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

# Definimos la función f(x)
def f(x):
    return ((x + 3) / 2)**2 - 2

# Definimos su derivada f'(x)
def f_prime(x):
    return (x + 3)/2

# Función para el método de Newton-Raphson (modificada para animación)
def newton_raphson_animation(f, f_prime, x0, tol=1e-4, max_iter=20):
    iterations = []
    x = x0
    for i in range(max_iter):
        fx = f(x)
        fpx = f_prime(x)
        x_new = x - fx / fpx
        iterations.append((x, x_new, fx, f(x_new)))
        if abs(x_new - x) < tol:
            break
        x = x_new
    return iterations

# Ejecutamos el método para ambos puntos iniciales
iter_x1 = newton_raphson_animation(f, f_prime, x0=-5)
iter_x2 = newton_raphson_animation(f, f_prime, x0=0)

# Obtenemos las soluciones finales
x1 = iter_x1[-1][1]
x2 = iter_x2[-1][1]
y_intersect = -2

print(f"Solución 1: x = {x1:.6f}")
print(f"Solución 2: x = {x2:.6f}")

# Configuración del gráfico
fig, ax = plt.subplots(figsize=(10, 6))
x_range = np.linspace(-10, 4, 400)
y_curve = f(x_range)

# Elementos estáticos
ax.plot(x_range, y_curve, 'b-', label=r'$y = \left(\frac{x+3}{2}\right)^2 - 2$')
ax.axhline(y_intersect, color='r', linestyle='--', label='$y = -2$')
ax.plot(x1, y_intersect, 'go', markersize=8)
ax.plot(x2, y_intersect, 'go', markersize=8)
ax.grid(True)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Método de Newton-Raphson: Búsqueda de raíces')
ax.set_xlim(-10, 4)
ax.set_ylim(-5, 10)
ax.axhline(0, color='k', linewidth=0.5)
ax.axvline(0, color='k', linewidth=0.5)

# Elementos animados
line1, = ax.plot([], [], 'g-', marker='o', markersize=6, label='Iteraciones x1')
line2, = ax.plot([], [], 'm-', marker='o', markersize=6, label='Iteraciones x2')
text_iter = ax.text(0.02, 0.95, '', transform=ax.transAxes)
ax.legend()

# Función de inicialización
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    text_iter.set_text('')
    return line1, line2, text_iter

# Función de animación mejorada
def animate(i):
    # Actualizar primera raíz
    x1_data, y1_data = [], []
    for step in range(min(i, len(iter_x1))):
        x, x_new, fx, fx_new = iter_x1[step]
        x1_data.extend([x, x_new])
        y1_data.extend([fx, 0])
    
    # Actualizar segunda raíz
    x2_data, y2_data = [], []
    for step in range(min(i, len(iter_x2))):
        x, x_new, fx, fx_new = iter_x2[step]
        x2_data.extend([x, x_new])
        y2_data.extend([fx, 0])
    
    line1.set_data(x1_data, y1_data)
    line2.set_data(x2_data, y2_data)
    
    # Mostrar información de iteración
    current_iter = min(i, max(len(iter_x1), len(iter_x2))-1)
    text_iter.set_text(f'Iteración {current_iter+1}')
    
    return line1, line2, text_iter

# Calculamos el número total de frames
total_frames = max(len(iter_x1), len(iter_x2)) + 2

# Creamos la animación
ani = animation.FuncAnimation(
    fig, animate, frames=total_frames,
    init_func=init, interval=600, blit=True
)

# Guardamos el GIF optimizado
try:
    writer = PillowWriter(fps=3)  # Reducimos FPS para mejor visualización
    ani.save('Ejercicio2.gif', writer=writer, dpi=100)
    print("Animación guardada como 'Ejercicio2.gif'")
except Exception as e:
    print(f"Error al guardar: {str(e)}")

plt.tight_layout()
plt.show()