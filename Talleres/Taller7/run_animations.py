import animate_iterations as animator
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

def show_message(title, text, color='black'):
    """Muestra un mensaje gráfico"""
    fig = plt.figure(figsize=(10, 6))
    plt.text(0.5, 0.7, title, ha='center', va='center', 
             fontsize=20, weight='bold', color=color)
    plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=14)
    if animator.ANIMATION_DIR:
        plt.text(0.5, 0.3, f"Ubicación de salida:\n{animator.ANIMATION_DIR}", 
                 ha='center', va='center', fontsize=12)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def verify_dependencies():
    """Verifica las dependencias necesarias"""
    try:
        import numpy
        import matplotlib
        from matplotlib.animation import FuncAnimation
        return True
    except ImportError as e:
        print(f"Error de dependencias: {str(e)}")
        print("Instala los requisitos con: pip install numpy matplotlib pillow")
        return False

def main():
    """Función principal"""
    if not verify_dependencies():
        show_message("Error de Dependencias", 
                    "Faltan paquetes necesarios\n\nEjecuta:\npip install numpy matplotlib pillow", 
                    color='red')
        return
    
    show_message("Generador de Animaciones", 
                "Métodos Iterativos\nGauss-Jacobi y Gauss-Seidel")
    
    try:
        animator.main()
        show_message("¡Proceso Completado!", 
                    "Las animaciones se generaron correctamente", 
                    color='green')
    except Exception as e:
        show_message("Error en la Ejecución", 
                    f"Ocurrió un error:\n{str(e)}\n\nRevisa animation_log.txt", 
                    color='red')
    finally:
        if os.name == 'nt':
            input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()