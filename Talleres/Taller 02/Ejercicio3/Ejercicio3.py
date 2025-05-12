import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

# Configuración para máxima velocidad
plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg'  # Asegúrate de tener FFmpeg instalado

# Función sinc optimizada
def sinc(x):
    return np.where(x != 0, np.sin(x)/x, 1.0)

# Parámetros optimizados
limite = 0.015
incremento = 0.05  # Incremento más grande para menos iteraciones
punto = 1.0

# Búsqueda optimizada
puntos = []
while True:
    if all(abs(sinc(punto + incremento * j)) < limite for j in range(100)):
        x_limite = punto
        break
    puntos.append(punto)
    punto += incremento

print(f"Punto encontrado: x = {x_limite:.2f} (en {len(puntos)} iteraciones)")

# Datos para el gráfico (solo zona relevante)
x_max = max(75, x_limite + 10)
dominio = np.linspace(0, x_max, 500)
imagen = sinc(dominio)

# Configuración del gráfico simplificada
fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
ax.plot(dominio, imagen, 'b-', lw=1.5, label='sinc(x)')
ax.axhline(limite, color='r', linestyle='--', lw=1, label=f'Límite: {limite}')
line_vert = ax.axvline(0, color='g', linestyle='-', lw=1.5, alpha=0.7)
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_xlim(0, x_max)
ax.set_ylim(-0.1, 1.1)

# Animación optimizada
def update(i):
    if i < len(puntos):
        x = puntos[i]
    else:
        x = x_limite
    line_vert.set_xdata([x, x])
    
    # Marcar el punto final
    if i == len(puntos):
        ax.plot(x, sinc(x), 'ro', ms=6)
        ax.text(x, 0.5, f' x = {x:.1f}', color='r', va='center')
    
    return line_vert,

skip = max(1, len(puntos)//100) 
ani = animation.FuncAnimation(
    fig, update, frames=range(0, len(puntos)+1, skip),
    interval=30, blit=True, repeat=False
)

# Guardar GIF optimizado
try:
    writer = PillowWriter(fps=20, bitrate=1800)
    ani.save('Ejercicio3.gif', writer=writer, dpi=100)
    print("¡GIF rápido generado: 'Ejercicio3.gif'!")
except Exception as e:
    print(f"Error: {e}")

plt.close()  