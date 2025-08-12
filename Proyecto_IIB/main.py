# main.py
"""
Punto de entrada principal para el Visualizador de Horizonte - Ecuador.
Inicia la aplicación de la interfaz gráfica.
"""

import sys
import math
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from config import DATA_DIR
import os

def main():

    # Verificar si la carpeta 'data' existe
    if not os.path.exists(DATA_DIR):
        print(f"Error: La carpeta de datos '{DATA_DIR}' no se encontró.")
        print("Asegúrese de que los archivos .hgt estén en la carpeta 'data' en el mismo directorio que 'main.py'.")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
