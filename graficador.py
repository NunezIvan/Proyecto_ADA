import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Graficador:
    """
    Maneja la generación de gráficos para visualizar las funciones de tiempo
    """
    
    def __init__(self, frame_parent):
        self.frame_parent = frame_parent
        # Tamaño de figura más pequeño y ajustado
        self.figura = plt.Figure(figsize=(3.5, 3), dpi=100)  # Reducido de (4,4) a (3.5,3)
        self.canvas = FigureCanvasTkAgg(self.figura, frame_parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def graficar_funcion(self, funcion_tiempo, titulo="Análisis de Complejidad"):
        """
        Grafica una función de tiempo
        """
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        
        # Generar valores para el eje x
        n_valores = np.array(range(1, 101))
        y_valores = funcion_tiempo.calcular_valores(n_valores)
        
        # Ajustes de estilo para espacio reducido
        ax.plot(n_valores, y_valores, 'b-', linewidth=1.5,  # Línea más delgada
                label=f'{funcion_tiempo.notacion_asintotica}')
        
        # Fuentes más pequeñas
        ax.set_xlabel('Tamaño de entrada (n)', fontsize=8)
        ax.set_ylabel('Tiempo de ejecución', fontsize=8)
        ax.set_title(titulo, fontsize=9, pad=10)  # pad reduce espacio sobre título
        ax.grid(True, alpha=0.3)
        
        # Leyenda más compacta
        ax.legend(fontsize=7, loc='upper left', bbox_to_anchor=(1, 1))
        
        # Ajustar márgenes y layout
        self.figura.subplots_adjust(left=0.15, bottom=0.15, right=0.85, top=0.85)
        self.canvas.draw()
    
    def graficar_comparacion(self, funciones_lista, titulo="Comparación de Complejidades"):
        """
        Grafica múltiples funciones para comparación
        """
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        
        n_valores = np.array(range(1, 101))
        colores = ['blue', 'red', 'green', 'orange', 'purple']
        
        for i, funcion in enumerate(funciones_lista):
            y_valores = funcion.calcular_valores(n_valores)
            color = colores[i % len(colores)]
            ax.plot(n_valores, y_valores, color=color, linewidth=1.5,  # Línea más delgada
                    label=funcion.notacion_asintotica)
        
        # Fuentes más pequeñas
        ax.set_xlabel('Tamaño de entrada (n)', fontsize=8)
        ax.set_ylabel('Tiempo de ejecución', fontsize=8)
        ax.set_title(titulo, fontsize=9, pad=10)
        ax.grid(True, alpha=0.3)
        
        # Leyenda externa más compacta
        ax.legend(fontsize=7, loc='center left', bbox_to_anchor=(1, 0.5))
        
        # Escala logarítmica si hay grandes diferencias
        max_valores = max([max(f.calcular_valores(n_valores)) for f in funciones_lista])
        if max_valores > 10000:
            ax.set_yscale('log')
        
        # Ajustar márgenes para mejor visualización
        self.figura.subplots_adjust(left=0.15, bottom=0.15, right=0.7, top=0.85)
        self.canvas.draw()