import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import newton

# Definimos la función f(x)
def f(x):
    return ((x + 3) / 2)**2 - 2

# Definimos su derivada f'(x)
def f_prime(x):
    return 2 * ((x + 3) / 2) * (1/2)

# Usamos dos valores iniciales distintos para encontrar ambas soluciones
x1 = newton(f, x0=-5, fprime=f_prime)
x2 = newton(f, x0=0, fprime=f_prime)

# Mostramos los resultados
print("Las intersecciones con y = -2 ocurren en los puntos:")
print(f"\nPunto de intersección 1: {x1:.4f}")
print(f"Punto de intersección 2: {x2:.4f}")

# Función para el método de Newton-Raphson
def newton_raphson(f, f_prime, x0, tol=1e-4, max_iter=20):
    iteraciones = []
    x = x0
    for i in range(max_iter):
        x_new = x - f(x) / f_prime(x)
        iteraciones.append((x, x_new, f(x_new)))
        if abs(x_new - x) < tol:
            break
        x = x_new
    return iteraciones

# Ejecutar el método de Newton-Raphson para ambos valores iniciales
iteraciones_x1 = newton_raphson(f, f_prime, x0=-5)
iteraciones_x2 = newton_raphson(f, f_prime, x0=0)

# Crear la animación
fig, ax = plt.subplots(figsize=(10, 6))

# El valor de y en las intersecciones es -2
y_intersect = -2

# Creamos un rango de valores de x para graficar la curva
x_range = np.linspace(-10, 4, 400)
y_curve_values = f(x_range)

# Graficamos la curva
ax.plot(x_range, y_curve_values, label=r'$y = \left(\frac{x+3}{2}\right)^2 - 2$')

# Graficamos la línea horizontal y = -2
ax.axhline(y=y_intersect, color='r', linestyle='--', label='$y = -2$')

# Marcamos los puntos de intersección
ax.plot(x1, y_intersect, 'go', markersize=8, label=f'Intersección 1: ({x1:.2f}, {y_intersect})')
ax.plot(x2, y_intersect, 'bo', markersize=8, label=f'Intersección 2: ({x2:.2f}, {y_intersect})')

# Añadimos etiquetas y título
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Intersección de la curva con la línea y = -2')
ax.grid(True)
ax.legend()
ax.set_ylim(-5, 10)
ax.set_xlim(-10, 4)
ax.axvline(x=0, color='black', linewidth=0.5)
ax.axhline(y=0, color='black', linewidth=0.5)
ax.axvline(x=x1, ymin=0, ymax=1, color='g', linestyle=':', linewidth=2)
ax.axvline(x=x2, ymin=0, ymax=1, color='b', linestyle=':', linewidth=2)
ax.set_aspect('equal', adjustable='box')  # Para que las escalas en x e y sean iguales

# Líneas para las iteraciones
line_x1, = ax.plot([], [], 'g--', label='Iteraciones x1')
line_x2, = ax.plot([], [], 'b--', label='Iteraciones x2')
text_iter = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def init():
    line_x1.set_data([], [])
    line_x2.set_data([], [])
    text_iter.set_text('')
    return line_x1, line_x2, text_iter

def animate(i):
    if i < len(iteraciones_x1):
        x, x_new, f_x_new = iteraciones_x1[i]
        line_x1.set_data([x, x_new], [f(x), f_x_new])
    else:
        line_x1.set_data([], [])
    
    if i < len(iteraciones_x2):
        x, x_new, f_x_new = iteraciones_x2[i]
        line_x2.set_data([x, x_new], [f(x), f_x_new])
    else:
        line_x2.set_data([], [])
    
    text_iter.set_text(f'Iteración {i+1}: x1={x1:.6f}, x2={x2:.6f}')
    return line_x1, line_x2, text_iter

# Crear la animación
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=max(len(iteraciones_x1), len(iteraciones_x2)), interval=500, blit=True)

# Guardar la animación como un archivo GIF
ani.save('Ejercicio_2.gif', writer='pillow')

# Mostrar la animación
plt.show()