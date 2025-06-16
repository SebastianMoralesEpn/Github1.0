import matplotlib.pyplot as plt
import numpy as np
from Blackbox import load_model, predict_point
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

# Configuración de estilos
COLOR_FONDO = "#f0f0f0"
COLOR_PRIMARIO = "#2c3e50"
COLOR_SECUNDARIO = "#3498db"
COLOR_TERCIARIO = "#e74c3c"
COLOR_EXITO = "#27ae60"
COLOR_TEXTO = "#2c3e50"
COLOR_GRAFICO = "#ecf0f1"

# Cargar el modelo
try:
    model = load_model()
    print("Modelo cargado exitosamente")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None

# Lista para guardar los puntos (x1, x2, clase)
puntos = []

def funcion_solucion(x):
    x_safe = np.where(x == 0, 1e-6, x)  # Para evitar división por cero
    return 0.10066 * np.sin(10.05 * x_safe) / x_safe + 0.00285
    

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Clasificación con Red Neuronal")
        self.root.configure(bg=COLOR_FONDO)
        self.mostrar_funcion = True  # Estado inicial: función visible
        
        # Configurar estilo
        self.configurar_estilos()
        
        # Frame para controles
        self.control_frame = tk.Frame(root, bg=COLOR_FONDO, padx=10, pady=10)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Frame para gráfico
        self.grafico_frame = tk.Frame(root, bg=COLOR_FONDO)
        self.grafico_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Controles
        self.crear_controles()
        
        # Gráfico inicial
        self.fig, self.ax = plt.subplots(figsize=(8, 5), facecolor=COLOR_GRAFICO)
        self.fig.patch.set_facecolor(COLOR_GRAFICO)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.grafico_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.dibujar_grafica()
    
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilo de los botones
        style.configure('TButton', 
                      font=('Helvetica', 10), 
                      borderwidth=1, 
                      relief="solid",
                      padding=5)
        
        style.map('Primary.TButton',
                 foreground=[('active', 'white'), ('!disabled', 'white')],
                 background=[('active', COLOR_SECUNDARIO), ('!disabled', COLOR_PRIMARIO)])
        
        style.map('Secondary.TButton',
                 foreground=[('active', 'white'), ('!disabled', 'white')],
                 background=[('active', COLOR_TERCIARIO), ('!disabled', COLOR_SECUNDARIO)])
        
        style.map('Danger.TButton',
                 foreground=[('active', 'white'), ('!disabled', 'white')],
                 background=[('active', '#c0392b'), ('!disabled', COLOR_TERCIARIO)])
        
        # Configurar estilo de las entradas
        style.configure('TEntry', 
                      fieldbackground='white', 
                      foreground=COLOR_TEXTO,
                      padding=5,
                      bordercolor=COLOR_PRIMARIO,
                      lightcolor=COLOR_PRIMARIO,
                      darkcolor=COLOR_PRIMARIO)
    
    def crear_controles(self):
        # Título
        titulo = tk.Label(self.control_frame, 
                        text="Clasificador de Puntos con Red Neuronal", 
                        font=('Helvetica', 14, 'bold'),
                        bg=COLOR_FONDO,
                        fg=COLOR_PRIMARIO)
        titulo.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Etiquetas y entradas
        tk.Label(self.control_frame, 
               text="Coordenada X₁ (0-4):", 
               bg=COLOR_FONDO,
               fg=COLOR_TEXTO,
               font=('Helvetica', 10)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        
        self.x1_entry = ttk.Entry(self.control_frame, style='TEntry')
        self.x1_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(self.control_frame, 
               text="Coordenada X₂ (-0.3-1.2):", 
               bg=COLOR_FONDO,
               fg=COLOR_TEXTO,
               font=('Helvetica', 10)).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        
        self.x2_entry = ttk.Entry(self.control_frame, style='TEntry')
        self.x2_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        # Botones
        self.evaluar_btn = ttk.Button(self.control_frame, 
                                   text="Evaluar Punto", 
                                   style='Primary.TButton',
                                   command=self.evaluar)
        self.evaluar_btn.grid(row=1, column=2, padx=5, pady=5, sticky='ew')
        
        # Botón para mostrar/ocultar función
        self.toggle_func_btn = ttk.Button(
            self.control_frame, 
            text="Ocultar Función Solución",
            style='Secondary.TButton',
            command=self.toggle_funcion
        )
        self.toggle_func_btn.grid(row=2, column=2, padx=5, pady=5, sticky='ew')
        
        # Botón para limpiar gráfico
        self.limpiar_btn = ttk.Button(
            self.control_frame,
            text="Limpiar Gráfico",
            style='Danger.TButton',
            command=self.limpiar_grafico
        )
        self.limpiar_btn.grid(row=1, column=3, padx=5, pady=5, sticky='ew', rowspan=2)
        
        # Área de mensajes
        self.mensaje_var = tk.StringVar()
        self.mensaje_label = tk.Label(self.control_frame, 
                                     textvariable=self.mensaje_var,
                                     font=('Helvetica', 10),
                                     bg=COLOR_FONDO,
                                     fg=COLOR_TERCIARIO,
                                     wraplength=400,
                                     justify='left')
        self.mensaje_label.grid(row=3, column=0, columnspan=4, pady=(10, 5), sticky='w')
        
        # Configurar peso de columnas para centrado
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(2, weight=1)
        self.control_frame.grid_columnconfigure(3, weight=1)
    
    def limpiar_grafico(self):
        """Limpia todos los puntos del gráfico"""
        global puntos
        puntos = []
        self.mensaje_var.set("Gráfico limpiado. Todos los puntos han sido eliminados.")
        self.mensaje_label.config(fg=COLOR_EXITO)
        self.dibujar_grafica()
    
    def toggle_funcion(self):
        """Alterna entre mostrar y ocultar la función solución"""
        self.mostrar_funcion = not self.mostrar_funcion
        
        # Actualizar texto del botón
        nuevo_texto = "Mostrar Función Solución" if not self.mostrar_funcion else "Ocultar Función Solución"
        self.toggle_func_btn.config(text=nuevo_texto)
        
        self.dibujar_grafica()
    
    def evaluar(self):
        # Obtener los valores de las entradas
        x1_str = self.x1_entry.get()
        x2_str = self.x2_entry.get()

        # Verificar si los valores son numéricos
        def es_numero(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        if not es_numero(x1_str) or not es_numero(x2_str):
            self.mensaje_var.set("Error: Ingrese valores numéricos válidos")
            self.mensaje_label.config(fg=COLOR_TERCIARIO)
            return

        try:
            x1_val = float(x1_str)
            x2_val = float(x2_str)
            
            if x1_val < 0 or x1_val > 4:
                self.mensaje_var.set("Error: X₁ debe estar entre 0 y 4")
                self.mensaje_label.config(fg=COLOR_TERCIARIO)
                return
            if x2_val < -0.3 or x2_val > 1.2:
                self.mensaje_var.set("Error: X₂ debe estar entre -0.3 y 1.2")
                self.mensaje_label.config(fg=COLOR_TERCIARIO)
                return
                
            if model is None:
                self.mensaje_var.set("Error: Modelo no cargado")
                self.mensaje_label.config(fg=COLOR_TERCIARIO)
                return
                
            clase = predict_point(model, x1_val, x2_val)
            puntos.append((x1_val, x2_val, clase))
            
            # Mensaje con estilo diferente para éxito
            self.mensaje_var.set(f"Punto evaluado: ({x1_val:.2f}, {x2_val:.2f}) → Clase: {clase}")
            self.mensaje_label.config(fg=COLOR_EXITO)
            
            self.dibujar_grafica()
            
        except Exception as e:
            self.mensaje_var.set(f"Error inesperado: {str(e)}")
            self.mensaje_label.config(fg=COLOR_TERCIARIO)
    
    def dibujar_grafica(self):
        self.ax.clear()
        
        # Configurar fondo y colores del gráfico
        self.ax.set_facecolor(COLOR_GRAFICO)
        self.fig.patch.set_facecolor(COLOR_GRAFICO)
        
        titulo = "Clasificación de Puntos con Red Neuronal"
        ylabel = "Coordenada X₂"
        
        if self.mostrar_funcion:
            titulo += " y Función Solución"
            ylabel += " / Función Solución"
            
            # Dibujar función solución con estilo mejorado
            x_vals = np.linspace(0, 4, 400)
            y_vals = funcion_solucion(x_vals)
            self.ax.plot(x_vals, y_vals, 
                        label="Función Solución f(X₁)", 
                        color='#9b59b6', 
                        linewidth=2.5,
                        linestyle='--',
                        alpha=0.8)
        
        # Dibujar puntos clasificados como puntos (círculos)
        if puntos:
            # Separar puntos por clase para mejor visualización
            clase_1 = [p for p in puntos if p[2] == 1.0]
            clase_0 = [p for p in puntos if p[2] == 0.0]
            
            # Dibujar puntos de clase 1 (azules)
            if clase_1:
                x1_1, x2_1, _ = zip(*clase_1)
                self.ax.scatter(x1_1, x2_1, 
                              color='#3498db', 
                              marker='o',
                              s=80,
                              edgecolors='white',
                              linewidths=1,
                              label="Clase 1",
                              alpha=0.8)
            
            # Dibujar puntos de clase 0 (rojos)
            if clase_0:
                x1_0, x2_0, _ = zip(*clase_0)
                self.ax.scatter(x1_0, x2_0, 
                              color='#e74c3c', 
                              marker='o',
                              s=80,
                              edgecolors='white',
                              linewidths=1,
                              label="Clase 0",
                              alpha=0.8)
        
        # Configurar gráfico con estilo profesional
        self.ax.set_title(titulo, fontsize=12, fontweight='bold', color=COLOR_PRIMARIO)
        self.ax.set_xlabel("Coordenada X₁", fontsize=10, color=COLOR_TEXTO)
        self.ax.set_ylabel(ylabel, fontsize=10, color=COLOR_TEXTO)
        
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_xlim(0, 4)
        self.ax.set_ylim(-0.3, 1.2)
        
        # Cambiar color de los ejes y ticks
        self.ax.spines['bottom'].set_color(COLOR_PRIMARIO)
        self.ax.spines['left'].set_color(COLOR_PRIMARIO)
        self.ax.tick_params(axis='x', colors=COLOR_TEXTO)
        self.ax.tick_params(axis='y', colors=COLOR_TEXTO)
        
        if self.mostrar_funcion or puntos:
            legend = self.ax.legend(facecolor=COLOR_GRAFICO, 
                                  edgecolor=COLOR_PRIMARIO,
                                  fontsize=9)
            for text in legend.get_texts():
                text.set_color(COLOR_TEXTO)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Configuración adicional de la ventana principal
    root.geometry("900x650")
    root.minsize(800, 600)
    
    # Establecer icono (opcional)
    try:
        root.iconbitmap('icon.ico')  # Reemplaza con la ruta a tu icono
    except:
        pass
    
    app = Aplicacion(root)
    root.mainloop()