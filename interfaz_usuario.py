import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from analizador_algoritmo import AnalizadorAlgoritmo
from funcion_tiempo import FuncionTiempo
from graficador import Graficador
from calculador_tiempo import CalculadorTiempo

class InterfazUsuario:
    """
    Maneja la interfaz gráfica de usuario
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Complejidad Algorítmica - UNMSM")
        self.root.geometry("1400x900")
        
        # Variables
        self.analizador = AnalizadorAlgoritmo()
        self.funcion_actual = None
        self.funciones_comparacion = []
        self.calculador_tiempo = CalculadorTiempo()
        self.inicializar_componentes()
        
    def inicializar_componentes(self):
        """
        Inicializa todos los componentes de la interfaz
        """
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_pestana_principal()
        self.crear_pestana_comparador()
        
    def crear_pestana_principal(self):
        """
        Crea la pestaña principal de análisis
        """
        # Frame principal
        main_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(main_frame, text="Análisis Principal")
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Analizador de Complejidad Algorítmica", 
                        font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Frame izquierdo - Entrada de código
        frame_codigo = ttk.LabelFrame(main_frame, text="Código a Analizar", padding="10")
        frame_codigo.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        frame_codigo.columnconfigure(0, weight=1)
        frame_codigo.rowconfigure(0, weight=1)
        
        # Área de texto para código con scroll horizontal
        self.texto_codigo = scrolledtext.ScrolledText(
            frame_codigo, 
            width=45, 
            height=25,
            font=("Courier", 10),
            wrap=tk.NONE,
            xscrollcommand=lambda *args: self._configurar_scroll_x(frame_codigo, *args)
        )
        self.texto_codigo.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Área de texto para código
        self.texto_codigo = scrolledtext.ScrolledText(frame_codigo, width=45, height=25,
                                                    font=("Courier", 10))
        self.texto_codigo.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar horizontal
        self.scroll_x_codigo = ttk.Scrollbar(frame_codigo, orient=tk.HORIZONTAL, command=self.texto_codigo.xview)
        self.scroll_x_codigo.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Botones de archivo
        frame_botones_archivo = ttk.Frame(frame_codigo)
        frame_botones_archivo.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(frame_botones_archivo, text="Cargar Archivo", 
                command=self.cargar_archivo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_archivo, text="Guardar Código", 
                command=self.guardar_codigo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_archivo, text="Limpiar", 
                command=self.limpiar_codigo).pack(side=tk.LEFT)
        
        # Botón de análisis
        self.boton_analizar = ttk.Button(frame_codigo, text="Analizar Algoritmo", 
                                        command=self.analizar_algoritmo)
        self.boton_analizar.grid(row=2, column=0, pady=(10, 0))
        
        # Frame derecho - Contenedor principal
        frame_derecho = ttk.Frame(main_frame)
        frame_derecho.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        frame_derecho.columnconfigure(0, weight=1)
        frame_derecho.rowconfigure(1, weight=1)
        
        # Frame superior derecho - Resultados del Análisis con scroll horizontal
        frame_resultados = ttk.LabelFrame(frame_derecho, text="Resultados del Análisis", padding="10")
        frame_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)
        
        self.texto_resultados = scrolledtext.ScrolledText(
            frame_resultados, 
            width=60, 
            height=15,
            font=("Courier", 9),
            wrap=tk.NONE,
            xscrollcommand=lambda *args: self._configurar_scroll_x(frame_resultados, *args)
        )
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.scroll_x_resultados = ttk.Scrollbar(frame_resultados, orient=tk.HORIZONTAL, command=self.texto_resultados.xview)
        self.scroll_x_resultados.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Área de resultados (ahora más grande)
        self.texto_resultados = scrolledtext.ScrolledText(frame_resultados, width=60, height=15,
                                                        font=("Courier", 9))
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame inferior derecho - Dividido en tiempo y gráficos
        frame_inferior = ttk.Frame(frame_derecho)
        frame_inferior.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        frame_inferior.columnconfigure(0, weight=1)
        frame_inferior.columnconfigure(1, weight=1)
        frame_inferior.rowconfigure(0, weight=1)
        
        # Frame de tiempo (ahora a la izquierda)
        frame_tiempo = ttk.LabelFrame(frame_inferior, text="Tiempo del Algoritmo", padding="10")
        frame_tiempo.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        frame_tiempo.columnconfigure(0, weight=1)
        frame_tiempo.rowconfigure(1, weight=1)
        
        # Contenido de tiempo
        self.texto_tiempo = scrolledtext.ScrolledText(frame_tiempo, width=40, height=15,
                                                    font=("Courier", 9))
        self.texto_tiempo.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones para funcionalidades de tiempo
        frame_botones_tiempo = ttk.Frame(frame_tiempo)
        frame_botones_tiempo.grid(row=1, column=0, pady=(5, 0))
        
        ttk.Button(frame_botones_tiempo, text="Medir Tiempo", 
                command=self.medir_tiempo_real).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_tiempo, text="Estimar", 
                command=self.estimar_tiempo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_tiempo, text="Proyección", 
                command=self.proyeccion_tiempo).pack(side=tk.LEFT)
        
        # Frame para gráficos (ahora más estrecho)
        frame_graficos = ttk.LabelFrame(frame_inferior, text="Visualización", padding="5")
        frame_graficos.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        frame_graficos.columnconfigure(0, weight=1)
        frame_graficos.rowconfigure(0, weight=1)
        
        # Inicializar graficador
        self.graficador = Graficador(frame_graficos)
        
        # Frame inferior - Comparación
        frame_comparacion = ttk.LabelFrame(main_frame, text="Comparación con Funciones Conocidas", padding="10")
        frame_comparacion.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Selección de funciones para comparar
        ttk.Label(frame_comparacion, text="Seleccionar funciones para comparar:").grid(row=0, column=0, sticky=tk.W)
        
        self.funciones_disponibles = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(n³)"]
        self.vars_comparacion = {}
        
        frame_checks = ttk.Frame(frame_comparacion)
        frame_checks.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        for i, funcion in enumerate(self.funciones_disponibles):
            var = tk.BooleanVar()
            self.vars_comparacion[funcion] = var
            ttk.Checkbutton(frame_checks, text=funcion, variable=var).grid(row=0, column=i, padx=5)
        
        ttk.Button(frame_comparacion, text="Comparar", 
                command=self.realizar_comparacion).grid(row=2, column=0, pady=(10, 0))
        
        # Agregar código de ejemplo
        self.agregar_ejemplo()
           
    def crear_pestana_comparador(self):
        """
        Crea la pestaña para comparar dos funciones ingresadas por el usuario
        """
        comparador_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(comparador_frame, text="Comparador de Funciones")
        
        # Configurar grid
        comparador_frame.columnconfigure(0, weight=1)
        comparador_frame.columnconfigure(1, weight=1)
        comparador_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo_comp = ttk.Label(comparador_frame, text="Comparador de Funciones", 
                               font=("Arial", 14, "bold"))
        titulo_comp.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Frame izquierdo - Función 1
        frame_func1 = ttk.LabelFrame(comparador_frame, text="Función 1", padding="10")
        frame_func1.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        frame_func1.columnconfigure(0, weight=1)
        frame_func1.rowconfigure(0, weight=1)
        
        # Área de código función 1
        self.texto_funcion1 = scrolledtext.ScrolledText(frame_func1, width=50, height=20,
                                                       font=("Courier", 10))
        self.texto_funcion1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones función 1
        frame_botones_f1 = ttk.Frame(frame_func1)
        frame_botones_f1.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(frame_botones_f1, text="Cargar Archivo", 
                  command=lambda: self.cargar_archivo_funcion(1)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_f1, text="Analizar Función 1", 
                  command=lambda: self.analizar_funcion_individual(1)).pack(side=tk.LEFT)
        
        # Frame derecho - Función 2
        frame_func2 = ttk.LabelFrame(comparador_frame, text="Función 2", padding="10")
        frame_func2.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        frame_func2.columnconfigure(0, weight=1)
        frame_func2.rowconfigure(0, weight=1)
        
        # Área de código función 2
        self.texto_funcion2 = scrolledtext.ScrolledText(frame_func2, width=50, height=20,
                                                       font=("Courier", 10))
        self.texto_funcion2.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones función 2
        frame_botones_f2 = ttk.Frame(frame_func2)
        frame_botones_f2.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(frame_botones_f2, text="Cargar Archivo", 
                  command=lambda: self.cargar_archivo_funcion(2)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_f2, text="Analizar Función 2", 
                  command=lambda: self.analizar_funcion_individual(2)).pack(side=tk.LEFT)
        
        # Frame inferior - Resultados de comparación
        frame_resultados_comp = ttk.LabelFrame(comparador_frame, text="Resultados de Comparación", padding="10")
        frame_resultados_comp.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        frame_resultados_comp.columnconfigure(0, weight=1)
        frame_resultados_comp.rowconfigure(0, weight=1)
        
        # Área de resultados comparación
        self.texto_resultados_comp = scrolledtext.ScrolledText(frame_resultados_comp, width=100, height=8,
                                                              font=("Courier", 9))
        self.texto_resultados_comp.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones de comparación
        frame_botones_comp = ttk.Frame(frame_resultados_comp)
        frame_botones_comp.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(frame_botones_comp, text="Comparar Funciones", 
                  command=self.comparar_funciones_usuarios).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(frame_botones_comp, text="Análisis Completo", 
                  command=self.analisis_completo_comparacion).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(frame_botones_comp, text="Limpiar", 
                  command=self.limpiar_comparador).pack(side=tk.LEFT)
        
        # Agregar ejemplos de comparación
        self.agregar_ejemplos_comparacion()
        
    def agregar_ejemplo(self):
        """
        Agrega un ejemplo de código para demostrar la funcionalidad
        """
        ejemplo = """# Ejemplo: Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Ejemplo de uso
lista = [64, 34, 25, 12, 22, 11, 90]
resultado = bubble_sort(lista)
print(resultado)
"""
        self.texto_codigo.insert(tk.END, ejemplo)
               
    def agregar_ejemplos_comparacion(self):
        """
        Agrega ejemplos de funciones para comparación
        """
        ejemplo1 = """# Algoritmo de ordenamiento burbuja
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""
        
        ejemplo2 = """# Algoritmo de ordenamiento rápido
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
"""
        
        self.texto_funcion1.insert(tk.END, ejemplo1)
        self.texto_funcion2.insert(tk.END, ejemplo2)
    
    # Métodos existentes (cargar_archivo, guardar_codigo, etc.)
    def cargar_archivo(self):
        """
        Carga un archivo de código Python
        """
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Python",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                self.texto_codigo.delete(1.0, tk.END)
                self.texto_codigo.insert(tk.END, contenido)
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    
    def guardar_codigo(self):
        """
        Guarda el código actual en un archivo
        """
        archivo = filedialog.asksaveasfilename(
            title="Guardar código",
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(self.texto_codigo.get(1.0, tk.END))
                messagebox.showinfo("Éxito", "Código guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}")
    
    def limpiar_codigo(self):
        """
        Limpia el área de código
        """
        self.texto_codigo.delete(1.0, tk.END)
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_tiempo.delete(1.0, tk.END)
        self.graficador.figura.clear()
        self.graficador.canvas.draw()
    
    def analizar_algoritmo(self):
        """Analiza el código y muestra los resultados"""
        codigo = self.texto_codigo.get("1.0", tk.END)
        
        if not codigo.strip():
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return
        
        try:
            # Reiniciar el analizador
            self.analizador = AnalizadorAlgoritmo()
            
            if self.analizador.analizar_codigo(codigo):
                # Obtener el resumen directamente como texto
                resumen_texto = self.analizador.obtener_resumen()
                
                # Mostrar resultados en el widget de texto correcto
                self.texto_resultados.delete("1.0", tk.END)
                self.texto_resultados.insert("1.0", resumen_texto)
                
                # Actualizar la función actual para comparaciones
                self.funcion_actual = FuncionTiempo()
                self.funcion_actual.generar_funcion(self.analizador.complejidad_detectada)
                
                # Actualizar sección de tiempo
                total_oe = self.analizador.detalles_analisis['operaciones_primitivas']
                self.actualizar_seccion_tiempo(total_oe)
                
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al analizar el código:\n{str(e)}")
    
    def _formatear_resumen(self, resumen_dict):
        """Convierte el diccionario de resumen a texto formateado"""
        texto = f"""
    ANÁLISIS DE COMPLEJIDAD ALGORÍTMICA
    =====================================

    Complejidad detectada: {resumen_dict.get('complejidad', 'Desconocida')}
    Función de tiempo estimada: {resumen_dict.get('funcion_tiempo', 'Desconocida')}

    DETALLES TÉCNICOS:
    ------------------
    """
        # Formatear detalles del análisis
        detalles = resumen_dict.get('detalles', {})
        if 'bucles' in detalles:
            texto += f"- Bucles FOR: {detalles['bucles'].get('for', 0)}\n"
            texto += f"- Bucles WHILE: {detalles['bucles'].get('while', 0)}\n"
            texto += f"- Bucles anidados: {detalles['bucles'].get('anidados', 0)}\n"
        
        if 'niveles_anidamiento' in detalles:
            texto += f"- Nivel máximo de anidamiento: {max(detalles['niveles_anidamiento'].keys(), default=0)}\n"
        
        texto += f"- Condicionales: {detalles.get('condicionales', 0)}\n"
        texto += f"- Llamadas a funciones: {detalles.get('llamadas_funciones', 0)}\n"
        
        if detalles.get('recursion', {}).get('detectada', False):
            texto += f"- Recursión: Sí ({detalles['recursion'].get('tipo', 'tipo no determinado')})\n"
        else:
            texto += "- Recursión: No\n"
        
        # Estructuras detectadas
        texto += "\nESTRUCTURAS DETECTADAS:\n----------------------\n"
        for estructura in resumen_dict.get('estructuras', []):
            texto += f"- {estructura}\n"
        
        return texto

    def realizar_comparacion(self):
        """
        Realiza la comparación con funciones seleccionadas
        """
        if not self.funcion_actual:
            messagebox.showwarning("Advertencia", "Primero debe analizar un algoritmo")
            return
        
        # Obtener funciones seleccionadas
        funciones_seleccionadas = [self.funcion_actual]
        
        for funcion_nombre, var in self.vars_comparacion.items():
            if var.get():
                funcion_comp = FuncionTiempo()
                funcion_comp.generar_funcion(funcion_nombre)
                funciones_seleccionadas.append(funcion_comp)
        
        if len(funciones_seleccionadas) == 1:
            messagebox.showwarning("Advertencia", "Seleccione al menos una función para comparar")
            return
        
        # Graficar comparación
        self.graficador.graficar_comparacion(funciones_seleccionadas, 
                                           "Comparación de Complejidades")
        
        # Mostrar comparación en texto
        resultado_comp = "\n\nCOMPARACIÓN DE EFICIENCIA:\n"
        resultado_comp += "=" * 30 + "\n"
        
        for funcion in funciones_seleccionadas[1:]:
            comparacion = self.funcion_actual.comparar(funcion)
            resultado_comp += f"vs {funcion.notacion_asintotica}: {comparacion}\n"
        
        self.texto_resultados.insert(tk.END, resultado_comp)
    
    # NUEVOS MÉTODOS PARA LAS FUNCIONALIDADES ADICIONALES
    
       
    def cargar_archivo_funcion(self, numero_funcion):
        """
        Carga archivo para función específica
        """
        archivo = filedialog.askopenfilename(
            title=f"Seleccionar archivo para Función {numero_funcion}",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                if numero_funcion == 1:
                    self.texto_funcion1.delete(1.0, tk.END)
                    self.texto_funcion1.insert(tk.END, contenido)
                else:
                    self.texto_funcion2.delete(1.0, tk.END)
                    self.texto_funcion2.insert(tk.END, contenido)
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    
    def analizar_funcion_individual(self, numero_funcion):
        """
        Analiza una función individual
        """
        if numero_funcion == 1:
            codigo = self.texto_funcion1.get(1.0, tk.END).strip()
        else:
            codigo = self.texto_funcion2.get(1.0, tk.END).strip()
        
        if not codigo:
            messagebox.showwarning("Advertencia", f"Por favor, ingrese código en la Función {numero_funcion}")
            return
        
        # Crear analizador temporal
        analizador_temp = AnalizadorAlgoritmo()
        
        if analizador_temp.analizar_codigo(codigo):
            resultado = f"ANÁLISIS FUNCIÓN {numero_funcion}:\n"
            resultado += "=" * 30 + "\n"
            resultado += f"Complejidad: {analizador_temp.complejidad_detectada}\n"
            resultado += f"Bucles FOR: {analizador_temp.detalles_analisis['bucles_for']}\n"
            resultado += f"Bucles WHILE: {analizador_temp.detalles_analisis['bucles_while']}\n"
            resultado += f"Nivel de anidamiento: {analizador_temp.detalles_analisis['nivel_anidamiento']}\n"
            resultado += f"Operaciones primitivas: {analizador_temp.detalles_analisis['operaciones_primitivas']}\n\n"
            
            self.texto_resultados_comp.insert(tk.END, resultado)
            messagebox.showinfo("Análisis Completado", 
                              f"Función {numero_funcion} analizada: {analizador_temp.complejidad_detectada}")
    
    def comparar_funciones_usuarios(self):
        """
        Compara las dos funciones ingresadas por el usuario
        """
        codigo1 = self.texto_funcion1.get(1.0, tk.END).strip()
        codigo2 = self.texto_funcion2.get(1.0, tk.END).strip()
        
        if not codigo1 or not codigo2:
            messagebox.showwarning("Advertencia", "Por favor, ingrese código en ambas funciones")
            return
        
        # Analizar ambas funciones
        analizador1 = AnalizadorAlgoritmo()
        analizador2 = AnalizadorAlgoritmo()
        
        if analizador1.analizar_codigo(codigo1) and analizador2.analizar_codigo(codigo2):
            # Crear funciones de tiempo
            funcion1 = FuncionTiempo()
            funcion1.generar_funcion(analizador1.complejidad_detectada)
            
            funcion2 = FuncionTiempo()
            funcion2.generar_funcion(analizador2.complejidad_detectada)
            
            # Mostrar comparación
            resultado = "\n" + "=" * 60 + "\n"
            resultado += "COMPARACIÓN DE FUNCIONES\n"
            resultado += "=" * 60 + "\n"
            
            resultado += f"FUNCIÓN 1: {analizador1.complejidad_detectada}\n"
            resultado += f"FUNCIÓN 2: {analizador2.complejidad_detectada}\n\n"
            
            comparacion = funcion1.comparar(funcion2)
            resultado += f"RESULTADO: Función 1 es {comparacion} que Función 2\n\n"
            
            # Detalles específicos
            resultado += "DETALLES FUNCIÓN 1:\n"
            resultado += f"- Bucles FOR: {analizador1.detalles_analisis['bucles_for']}\n"
            resultado += f"- Bucles WHILE: {analizador1.detalles_analisis['bucles_while']}\n"
            resultado += f"- Nivel anidamiento: {analizador1.detalles_analisis['nivel_anidamiento']}\n"
            resultado += f"- Operaciones primitivas: {analizador1.detalles_analisis['operaciones_primitivas']}\n\n"
            
            resultado += "DETALLES FUNCIÓN 2:\n"
            resultado += f"- Bucles FOR: {analizador2.detalles_analisis['bucles_for']}\n"
            resultado += f"- Bucles WHILE: {analizador2.detalles_analisis['bucles_while']}\n"
            resultado += f"- Nivel anidamiento: {analizador2.detalles_analisis['nivel_anidamiento']}\n"
            resultado += f"- Operaciones primitivas: {analizador2.detalles_analisis['operaciones_primitivas']}\n"
            
            self.texto_resultados_comp.insert(tk.END, resultado)
            
            messagebox.showinfo("Comparación Completada", 
                              f"Función 1: {analizador1.complejidad_detectada}\n"
                              f"Función 2: {analizador2.complejidad_detectada}")
    
    def analisis_completo_comparacion(self):
        """
        Realiza un análisis completo de ambas funciones con gráficos
        """
        codigo1 = self.texto_funcion1.get(1.0, tk.END).strip()
        codigo2 = self.texto_funcion2.get(1.0, tk.END).strip()
        
        if not codigo1 or not codigo2:
            messagebox.showwarning("Advertencia", "Por favor, ingrese código en ambas funciones")
            return
        
        # Analizar ambas funciones
        analizador1 = AnalizadorAlgoritmo()
        analizador2 = AnalizadorAlgoritmo()
        
        if analizador1.analizar_codigo(codigo1) and analizador2.analizar_codigo(codigo2):
            # Crear funciones de tiempo
            funcion1 = FuncionTiempo()
            funcion1.generar_funcion(analizador1.complejidad_detectada)
            funcion1.notacion_asintotica = f"Función 1: {analizador1.complejidad_detectada}"
            
            funcion2 = FuncionTiempo()
            funcion2.generar_funcion(analizador2.complejidad_detectada)
            funcion2.notacion_asintotica = f"Función 2: {analizador2.complejidad_detectada}"
            
            # Crear gráfico en la pestaña principal
            self.notebook.select(0)  # Cambiar a pestaña principal
            self.graficador.graficar_comparacion([funcion1, funcion2], 
                                               "Comparación Detallada de Funciones")
            
            # Mostrar análisis completo
            resultado = "\n" + "=" * 80 + "\n"
            resultado += "ANÁLISIS COMPLETO DE COMPARACIÓN\n"
            resultado += "=" * 80 + "\n"
            
            resultado += "FUNCIÓN 1:\n"
            resultado += "-" * 40 + "\n"
            resultado += analizador1.obtener_resumen() + "\n"
            
            resultado += "FUNCIÓN 2:\n"
            resultado += "-" * 40 + "\n"
            resultado += analizador2.obtener_resumen() + "\n"
            
            resultado += "ANÁLISIS COMPARATIVO:\n"
            resultado += "-" * 40 + "\n"
            comparacion = funcion1.comparar(funcion2)
            resultado += f"Eficiencia: Función 1 es {comparacion} que Función 2\n\n"
            
            # Recomendaciones
            resultado += "RECOMENDACIONES:\n"
            resultado += "-" * 40 + "\n"
            if "Más eficiente" in comparacion:
                resultado += "• Se recomienda usar la Función 1 para mejor rendimiento\n"
            elif "Menos eficiente" in comparacion:
                resultado += "• Se recomienda usar la Función 2 para mejor rendimiento\n"
            else:
                resultado += "• Ambas funciones tienen eficiencia similar\n"
            
            resultado += "• Considere el contexto específico de uso\n"
            resultado += "• Evalúe otros factores como legibilidad y mantenibilidad\n"
            
            self.texto_resultados.delete(1.0, tk.END)
            self.texto_resultados.insert(tk.END, resultado)
            
            messagebox.showinfo("Análisis Completo", 
                              "Análisis completo realizado. Revise los resultados en la pestaña principal.")
    
    def limpiar_comparador(self):
        """
        Limpia las áreas del comparador
        """
        self.texto_funcion1.delete(1.0, tk.END)
        self.texto_funcion2.delete(1.0, tk.END)
        self.texto_resultados_comp.delete(1.0, tk.END)
        self.agregar_ejemplos_comparacion()
    
    # MÉTODOS PARA LA SECCIÓN DE TIEMPO (PREPARADOS PARA IMPLEMENTAR)
    
    def medir_tiempo_real(self):
        """
        Mide el tiempo real de ejecución del algoritmo
        """
        codigo = self.texto_codigo.get(1.0, tk.END).strip()
        
        if not codigo:
            messagebox.showwarning("Advertencia", "Por favor, ingrese código para medir")
            return
        
        try:
            # Crear un entorno seguro para ejecutar el código
            local_vars = {}
            global_vars = {}
            
            # Ejecutar el código para medir tiempo
            import time
            inicio = time.time()
            exec(codigo, global_vars, local_vars)
            tiempo_ejecucion = time.time() - inicio
            
            # Mostrar resultados
            tiempo_info = f"""
RESULTADOS DE MEDICIÓN REAL
==========================

Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos

Detalles:
• Código ejecutado con los valores por defecto
• Ambiente controlado sin entradas externas
• Tiempo puede variar según el hardware

Recomendaciones:
• Ejecute varias veces para obtener un promedio
• Pruebe con diferentes tamaños de entrada
"""
            
            self.texto_tiempo.delete(1.0, tk.END)
            self.texto_tiempo.insert(tk.END, tiempo_info)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar el código: {str(e)}")
    
    def estimar_tiempo(self):
        """
        Estima el tiempo de ejecución basado en la complejidad
        """
        if not self.funcion_actual:
            messagebox.showwarning("Advertencia", "Primero debe analizar un algoritmo")
            return
        
        # Obtener el número base de OE
        codigo = self.texto_codigo.get(1.0, tk.END).strip()
        total_oe = self.calculador_tiempo.analizar_codigo(codigo)
        
        # Crear ventana para entrada de n
        ventana_estimacion = tk.Toplevel(self.root)
        ventana_estimacion.title("Estimación de Tiempo")
        ventana_estimacion.geometry("400x300")
        
        tk.Label(ventana_estimacion, text="Ingrese el tamaño de entrada (n):").pack(pady=10)
        
        entrada_n = tk.Entry(ventana_estimacion)
        entrada_n.pack(pady=5)
        entrada_n.insert(0, "100")
        
        tk.Label(ventana_estimacion, text="OE por segundo (estimado):").pack(pady=5)
        
        entrada_oe_por_seg = tk.Entry(ventana_estimacion)
        entrada_oe_por_seg.pack(pady=5)
        entrada_oe_por_seg.insert(0, "1000000")
        
        resultado = tk.Text(ventana_estimacion, height=8, width=50)
        resultado.pack(pady=10)
        
        def calcular_estimacion():
            try:
                n = int(entrada_n.get())
                oe_por_seg = float(entrada_oe_por_seg.get())
                
                oe_estimados = self._estimar_oe(n, total_oe)
                tiempo_estimado = oe_estimados / oe_por_seg
                
                resultado.delete(1.0, tk.END)
                resultado.insert(tk.END, 
                    f"Para n = {n}:\n"
                    f"OE estimados: {oe_estimados}\n"
                    f"Tiempo estimado: {tiempo_estimado:.6f} segundos\n\n"
                    f"Complejidad: {self.analizador.complejidad_detectada}\n"
                    f"OE base: {total_oe}"
                )
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos")
        
        tk.Button(ventana_estimacion, text="Calcular", command=calcular_estimacion).pack(pady=5)
    
    def proyeccion_tiempo(self):
        """
        Proyecta el tiempo para diferentes tamaños de entrada
        """
        if not self.funcion_actual:
            messagebox.showwarning("Advertencia", "Primero debe analizar un algoritmo")
            return
        
        # Obtener el número base de OE
        codigo = self.texto_codigo.get(1.0, tk.END).strip()
        total_oe = self.calculador_tiempo.analizar_codigo(codigo)
        
        # Calcular proyecciones
        tamanos = [10, 100, 1000, 10000, 100000]
        resultados = []
        
        for n in tamanos:
            oe = self._estimar_oe(n, total_oe)
            tiempo = oe / 1e6  # Asumiendo 1 millón de OE por segundo
            resultados.append((n, oe, tiempo))
        
        # Mostrar resultados
        proyeccion_info = "PROYECCIÓN DE TIEMPO PARA DIFERENTES TAMAÑOS\n"
        proyeccion_info += "="*60 + "\n\n"
        proyeccion_info += "┌─────────────┬──────────────────┬──────────────────────┐\n"
        proyeccion_info += "│ Tamaño (n)  │ OE estimados     │ Tiempo estimado (s)  │\n"
        proyeccion_info += "├─────────────┼──────────────────┼──────────────────────┤\n"
        
        for n, oe, tiempo in resultados:
            proyeccion_info += f"│ {n:<11} │ {oe:<16} │ {tiempo:<20.6f} │\n"
        
        proyeccion_info += "└─────────────┴──────────────────┴──────────────────────┘\n\n"
        proyeccion_info += f"Nota: Asumiendo 1,000,000 OE por segundo\n"
        proyeccion_info += f"Complejidad: {self.analizador.complejidad_detectada}\n"
        proyeccion_info += f"OE base: {total_oe}"
        
        self.texto_tiempo.delete(1.0, tk.END)
        self.texto_tiempo.insert(tk.END, proyeccion_info)
    
    def actualizar_seccion_tiempo(self, total_oe):
        """
        Actualiza la sección de tiempo con información detallada
        """
        if not self.funcion_actual:
            return
        
        info_tiempo = f"""
INFORMACIÓN DE TIEMPO DE EJECUCIÓN
==================================

Detalles del cálculo:
• Cada operación elemental (OE) toma 1 unidad de tiempo
• T(n) = Número total de OE
• Complejidad temporal: {self.analizador.complejidad_detectada}

Ejemplo de estimación:
Para n = 1000:
• OE esperados: {self._estimar_oe(1000, total_oe)}
• Tiempo estimado: {self._estimar_tiempo(1000, total_oe):.6f} segundos (asumiendo 1e6 OE/seg)

Utilice los botones para:
• Medir tiempo real con diferentes entradas
• Proyectar tiempos para diferentes tamaños de n
"""
        
        self.texto_tiempo.delete(1.0, tk.END)
        self.texto_tiempo.insert(tk.END, info_tiempo)

    
    def _estimar_oe(self, n, base_oe):
            """Estima OE para un tamaño n dado"""
            complejidad = self.analizador.complejidad_detectada
            if "O(1)" in complejidad:
                return base_oe
            elif "O(n)" in complejidad:
                return base_oe * n
            elif "O(n^2)" in complejidad or "O(n²)" in complejidad:
                return base_oe * n * n
            elif "O(log n)" in complejidad:
                return base_oe * (n.bit_length() + 1)
            elif "O(n log n)" in complejidad:
                return base_oe * n * (n.bit_length() + 1)
            else:
                return base_oe * n  # Por defecto, asumir lineal
            
    def _estimar_tiempo(self, n, base_oe):
        """Estima tiempo en segundos para un tamaño n"""
        oe = self._estimar_oe(n, base_oe)
        return oe / 1e6  # Asumiendo 1 millón de OE por segundo
    
    def _configurar_scroll_x(self, frame, *args):
        """Configura el scroll horizontal para los widgets de texto"""
        self.scroll_x_codigo.set(*args)
        # Ajustar visibilidad del scrollbar
        if float(args[1]) > 0:
            self.scroll_x_codigo.grid()
        else:
            self.scroll_x_codigo.grid_remove()