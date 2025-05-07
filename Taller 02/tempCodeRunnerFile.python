import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import newton

# Definir la función f(x)
def f(x):
    return np.sin(x) / x

# Definir la ecuación f(x) - 0.015 = 0
def equation(x):
    return np.sin(x) / x - 0.015

# Implementar el método de Newton manualmente para obtener las iteraciones
def newton_steps(func, x0, tol=1e-6, max_iter=20):
    x = x0
    steps = [x]
    for _ in range(max_iter):
        fx = func(x)
        dfx = (func(x + tol) - fx) / tol  # Aproximación de la derivada
        if abs(fx) < tol:
            break
        x -= fx / dfx
        steps.append(x)
    return steps

# Punto inicial
x0 = 20
steps = newton_steps(equation, x0)
xT = steps[-1]  # Última iteración, valor convergente

# Crear el dominio para la gráfica
x_vals = np.linspace(0.1, xT + 5, 1000)
y_vals = f(x_vals)

# Configurar la figura
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x_vals, y_vals, label=r'$f(x) = \frac{\sin(x)}{x}$', color='blue')
ax.axhline(0.015, color='red', linestyle='--', label=r'$f(x) = 0.015$')
ax.set_title('Proceso iterativo del método de Newton')
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.legend()
ax.grid(True)

# Inicializar el punto y la línea vertical
point, = ax.plot([], [], 'ro', markersize=8)
vline = ax.axvline(steps[0], color='green', linestyle='--')

# Función de inicialización
def init():
    point.set_data([], [])
    vline.set_xdata(steps[0])
    ax.set_xlim(steps[0] - 5, steps[0] + 5)  # Inicializar zoom en la primera iteración
    return point, vline

# Función de actualización de la animación
def update(frame):
    x_current = steps[frame]
    y_current = f(x_current)
    
    point.set_data(x_current, y_current)
    vline.set_xdata(x_current)
    
    # Mover la ventana de visualización
    ax.set_xlim(x_current - 5, x_current + 5)

    return point, vline

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=len(steps), init_func=init, blit=True, interval=500)

# Mostrar la animación
plt.show()
