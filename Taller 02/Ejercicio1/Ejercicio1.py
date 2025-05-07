import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Definición de la función
def f(x):
    return x**4 + 540*x**3 + 109124*x**2 + 9781632*x + 328188672

# Implementación del método de la bisección
def biseccion(f, a, b, tolera, iteramax=20):
    if f(a) * f(b) > 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b].")
    
    iteraciones = []
    for i in range(iteramax):
        c = (a + b) / 2
        fc = f(c)
        iteraciones.append((a, b, c, fc))
        
        if abs(fc) < tolera or (b - a) / 2 < tolera:
            break
        
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    
    return iteraciones

# Parámetros iniciales
a = -140
b = 100
tolera = 1e-4

# Verificar si la función cambia de signo en el intervalo
if f(a) * f(b) > 0:
    raise ValueError(f"La función no cambia de signo en el intervalo [{a}, {b}].")

# Ejecutar el método de la bisección
iteraciones = biseccion(f, a, b, tolera)

# Crear la animación
fig, ax = plt.subplots()
x = np.linspace(a, b, 400)
y = f(x)

ax.plot(x, y, 'b-', label='f(x) = x^4 + 540x^3 + 109124x^2 + 9781632x + 328188672')
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_title('Método de la Bisección')
ax.grid(True)

# Líneas para a, b, c
line_a, = ax.plot([], [], 'ro-', label='a')
line_b, = ax.plot([], [], 'go-', label='b')
line_c, = ax.plot([], [], 'ko-', label='c')
text_iter = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def init():
    line_a.set_data([], [])
    line_b.set_data([], [])
    line_c.set_data([], [])
    text_iter.set_text('')
    return line_a, line_b, line_c, text_iter

def animate(i):
    a_i, b_i, c_i, fc_i = iteraciones[i]
    line_a.set_data([a_i, a_i], [0, f(a_i)])
    line_b.set_data([b_i, b_i], [0, f(b_i)])
    line_c.set_data([c_i, c_i], [0, f(c_i)])
    text_iter.set_text(f'Iteración {i+1}: a={a_i:.6f}, b={b_i:.6f}, c={c_i:.6f}, f(c)={fc_i:.6f}')
    return line_a, line_b, line_c, text_iter

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(iteraciones), interval=500, blit=True)

# Mostrar la leyenda
ax.legend()

# Guardar la animación como un archivo GIF
ani.save('Ejercicio_1.gif', writer='pillow')

# Mostrar la animación
plt.show()