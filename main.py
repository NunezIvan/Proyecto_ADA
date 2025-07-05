from controlador import Controlador
from tkinter import messagebox

def main():
    """
    Función principal
    """
    print("=" * 60)
    print("ANALIZADOR DE COMPLEJIDAD ALGORÍTMICA")
    print("=" * 60)
    print("Desarrollado por: Castro, Carrascal, Bayona, Nuñez, Gil")
    print("Universidad Nacional Mayor de San Marcos")
    print("Facultad de Ingeniería de Sistemas e Informática")
    print("=" * 60)
    print("Iniciando aplicación...")
    print("=" * 60)
    
    try:
        app = Controlador()
        app.ejecutar()
    except ImportError as e:
        error_msg = f"Error de importación: {str(e)}\n\n"
        error_msg += "Asegúrese de tener instaladas todas las dependencias:\n"
        error_msg += "pip install matplotlib numpy"
        print(error_msg)
        messagebox.showerror("Error de Dependencias", error_msg)
    except Exception as e:
        error_msg = f"Error al iniciar la aplicación: {str(e)}"
        print(error_msg)
        messagebox.showerror("Error Fatal", error_msg)

if __name__ == "__main__":
    main()