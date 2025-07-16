import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from src import gauss_jacobi, gauss_seidel
import os
import sys
from pathlib import Path
import logging

# Configuración inicial de logging
def setup_logging():
    """Configura el sistema de logging de forma robusta"""
    log_dir = Path(__file__).parent
    log_file = log_dir / "animation_log.txt"
    
    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(log_file, mode='w')
            ]
        )
        logging.info("Sistema de logging configurado correctamente")
        return True
    except Exception as e:
        print(f"No se pudo configurar el logging: {str(e)}")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        logging.warning("Usando solo logging en consola")
        return False

# Configuración de ejecución
TOL = 1e-6
MAX_ITER = 50

def get_animation_directory():
    """Obtiene un directorio válido para guardar animaciones"""
    possible_dirs = [
        # 1. Directorio específico solicitado
        Path(r"C:\Users\PC\Documents\Github1.0\Talleres\Taller7\animations"),
        
        # 2. Directorio del script
        Path(__file__).parent / "animations",
        
        # 3. Directorio temporal
        Path(os.getenv('TEMP', '.')) / "iterative_methods_animations"
    ]
    
    for dir_path in possible_dirs:
        try:
            dir_path.mkdir(exist_ok=True)
            test_file = dir_path / "write_test.tmp"
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            logging.info(f"Usando directorio de salida: {dir_path}")
            return dir_path
        except Exception as e:
            logging.warning(f"No se pudo usar {dir_path}: {str(e)}")
            continue
    
    logging.error("No se encontró ningún directorio válido para guardar animaciones")
    return None

# Configurar logging y directorio de salida
setup_logging()
ANIMATION_DIR = get_animation_directory()

def create_animation(A, b, x0, method, system_name, position_num):
    """Crea y guarda la animación de la trayectoria"""
    if ANIMATION_DIR is None:
        logging.error("No hay directorio de salida válido")
        return False
    
    try:
        # Obtener trayectoria
        if method.lower() == "jacobi":
            _, tray = gauss_jacobi(A=A, b=b, x0=x0, tol=TOL, max_iter=MAX_ITER)
        else:
            _, tray = gauss_seidel(A=A, b=b, x0=x0, tol=TOL, max_iter=MAX_ITER)
        
        if not tray or len(tray) < 2:
            logging.warning("Trayectoria demasiado corta para animación")
            return False
            
        tray_array = np.vstack([np.array(x).flatten() for x in tray])
    except Exception as e:
        logging.error(f"Error al obtener trayectoria: {str(e)}")
        return False

    # Configurar figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Configurar rangos dinámicos
    x_min, x_max = np.min(tray_array[:, 0]), np.max(tray_array[:, 0])
    y_min, y_max = np.min(tray_array[:, 1]), np.max(tray_array[:, 1])
    x_pad, y_pad = max(1, 0.2*(x_max-x_min)), max(1, 0.2*(y_max-y_min))
    
    # Graficar ecuaciones
    x_vals = np.linspace(x_min-x_pad, x_max+x_pad, 400)
    for i in range(A.shape[0]):
        if A[i, 1] != 0:
            y_vals = (b[i] - A[i, 0]*x_vals)/A[i, 1]
            ax.plot(x_vals, y_vals, '--', linewidth=2, alpha=0.7, 
                    label=f'{A[i,0]}x₁ + {A[i,1]}x₂ = {b[i]}')

    # Elementos de animación
    line, = ax.plot([], [], 'b-', linewidth=1.5, alpha=0.6, label='Trayectoria')
    points = ax.scatter([], [], color='blue', s=30, alpha=0.5)
    start_point = ax.scatter([], [], color='red', s=150, 
                           edgecolor='black', label='Inicio')
    current_point = ax.scatter([], [], color='green', s=150, 
                             edgecolor='black', label='Iteración')

    # Configuración del gráfico
    ax.set(xlim=(x_min-x_pad, x_max+x_pad), 
           ylim=(y_min-y_pad, y_max+y_pad),
           xlabel='x₁', ylabel='x₂',
           title=f"{system_name} - {method} (Inicial {position_num})")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='best')

    # Funciones de animación
    def init():
        # Línea vacía al inicio
        line.set_data([], [])
        
        # Dibujar solo el punto de inicio al comienzo
        start_point.set_offsets(tray_array[0, :])
        
        # Los puntos de iteración y el punto actual estarán vacíos al inicio
        points.set_offsets(np.empty((0, 2)))
        current_point.set_offsets(tray_array[0, :])  # Mostrar también en el inicio
        
        return line, points, start_point, current_point

    def update(frame):
        # Actualizar la línea y los puntos hasta la iteración actual
        line.set_data(tray_array[:frame+1, 0], tray_array[:frame+1, 1])
        points.set_offsets(tray_array[:frame+1, :])
        
        # El punto de inicio se mantiene fijo, ya está seteado en init()
        
        # El punto actual se actualiza siempre
        current_point.set_offsets(tray_array[frame, :])
        
        ax.set_title(f"{system_name} - {method} (Inicial {position_num})\nIteración {frame+1}/{len(tray_array)}")
        return line, points, start_point, current_point

    # Crear y guardar animación
    try:
        anim = FuncAnimation(fig, update, frames=len(tray_array),
                            init_func=init, blit=True, interval=300)
        
        filename = f"{system_name.lower().replace(' ', '_')}_{method.lower()}_init_{position_num}.gif"
        filepath = ANIMATION_DIR / filename
        
        # Intentar con diferentes métodos de guardado
        writers = ['pillow', 'ffmpeg']
        for writer in writers:
            try:
                anim.save(filepath, writer=writer, fps=3, dpi=100)
                logging.info(f"Animación guardada en: {filepath}")
                plt.close()
                return True
            except Exception as e:
                logging.warning(f"No se pudo guardar con {writer}: {str(e)}")
                continue
        
        raise Exception("No se encontró un método válido para guardar la animación")
        
    except Exception as e:
        logging.error(f"Error al guardar animación: {str(e)}")
        plt.close()
        return False
    finally:
        plt.close('all')

def run_system(A, b, system_name, initials):
    """Ejecuta las animaciones para un sistema"""
    logging.info(f"\n{'='*40}\nProcesando {system_name}\n{'='*40}")
    
    for i, x0 in enumerate(initials, 1):
        logging.info(f"\n• Posición inicial {i}: {x0}")
        
        # Jacobi
        logging.info("Ejecutando Jacobi...")
        success_j = create_animation(A, b, x0, "Jacobi", system_name, i)
        
        # Gauss-Seidel
        logging.info("Ejecutando Gauss-Seidel...")
        success_gs = create_animation(A, b, x0, "Seidel", system_name, i)
        
        if not success_j or not success_gs:
            logging.warning(f"Problemas con posición inicial {i}")

def main():
    """Función principal"""
    if ANIMATION_DIR is None:
        logging.error("""
        No se pudo establecer un directorio de salida válido.
        Por favor:
        1. Crea manualmente la carpeta 'animations' en:
           C:\\Users\\PC\\Documents\\Github1.0\\Talleres\\Taller7\\
        2. Verifica los permisos de escritura
        """)
        return
    
    logging.info(f"Las animaciones se guardarán en: {ANIMATION_DIR}")
    
    # Sistema 1
    A1 = np.array([[1, 1], [-2, 5]])
    b1 = np.array([7, 0])
    initials_s1 = [np.array([5, 2]), np.array([0, 0]), np.array([-2, 4])]
    run_system(A1, b1, "Sistema 1", initials_s1)
    
    # Sistema 2
    A2 = np.array([[1, 1], [-2, 1]])
    b2 = np.array([6, 0])
    initials_s2 = [np.array([5, 2]), np.array([0, 0]), np.array([-2, 4])]
    run_system(A2, b2, "Sistema 2", initials_s2)
    
    logging.info("\nProceso completado. Revisa el directorio de animaciones.")

if __name__ == "__main__":
    main()