import tkinter as tk
from tkinter import messagebox
from interfaz_usuario import InterfazUsuario

class Controlador:  
    def __init__(self):
        self.root = tk.Tk()
        self.interfaz = InterfazUsuario(self.root)
        
    def ejecutar(self):
        """
        Inicia la aplicación
        """
        self.root.mainloop()