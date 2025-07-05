import ast
from tkinter import messagebox
import math
from analizador_while import AnalizadorWhile

class AnalizadorAlgoritmo:
    """
    Clase encargada de analizar el código fuente y determinar su complejidad temporal
    basada en operaciones elementales y estructuras de control.
    """
    
    def __init__(self):
        self.codigo_fuente = ""
        self.estructura_analizada = []
        self.complejidad_detectada = "O(1)"
        self.funcion_tiempo = ""
        self.analizador_while = AnalizadorWhile()
        self.detalles_analisis = {
            'bucles_for': 0,
            'bucles_while': 0,
            'bucles_anidados': 0,
            'nivel_anidamiento': 0,
            'operaciones_primitivas': 0,
            'condicionales': 0,
            'funciones': 0,
            'max_iteraciones': 1,
            'oe_por_iteracion': 0
        }
        
    def analizar_codigo(self, codigo):
        """
        Analiza el código fuente usando AST para detectar estructuras relevantes
        y calcular la complejidad temporal.
        """
        self.codigo_fuente = codigo
        self._reset_analisis()
        
        try:
            tree = ast.parse(codigo)
            self._visitar_nodos(tree, 0)
            self._determinar_complejidad()
            self._calcular_funcion_tiempo()
            return True
            
        except SyntaxError as e:
            messagebox.showerror("Error de Sintaxis", f"Error en el código: {str(e)}")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el código: {str(e)}")
            return False
    
    def _reset_analisis(self):
        """Reinicia los contadores de análisis"""
        self.estructura_analizada = []
        self.detalles_analisis = {
            'bucles_for': 0,
            'bucles_while': 0,
            'bucles_anidados': 0,
            'nivel_anidamiento': 0,
            'operaciones_primitivas': 0,
            'condicionales': 0,
            'funciones': 0,
            'max_iteraciones': 1,
            'oe_por_iteracion': 0
        }
        self.complejidad_detectada = "O(1)"
        self.funcion_tiempo = ""
    
    def _visitar_nodos(self, node, nivel_actual):
        """
        Visita recursivamente todos los nodos del AST y cuenta operaciones elementales.
        """
        # Contar operaciones elementales
        if isinstance(node, ast.Assign):
            self.detalles_analisis['operaciones_primitivas'] += 1
        elif isinstance(node, ast.AugAssign):
            self.detalles_analisis['operaciones_primitivas'] += 2  # Operación + asignación
        elif isinstance(node, ast.BinOp):
            self.detalles_analisis['operaciones_primitivas'] += 1
        elif isinstance(node, ast.Compare):
            self.detalles_analisis['operaciones_primitivas'] += len(node.ops)
        elif isinstance(node, ast.Call):
            self.detalles_analisis['funciones'] += 1
            self.detalles_analisis['operaciones_primitivas'] += 1  # 1 OE por llamada
            
        # Manejar estructuras de control
        if isinstance(node, ast.For):
            self._procesar_bucle_for(node, nivel_actual)
        elif isinstance(node, ast.While):
            self._procesar_bucle_while(node, nivel_actual)
        elif isinstance(node, ast.If):
            self._procesar_condicional(node, nivel_actual)
            
        # Visitar nodos hijos
        for child in ast.iter_child_nodes(node):
            self._visitar_nodos(child, nivel_actual)
    
    def _procesar_bucle_for(self, node, nivel_actual):
        """Procesa un bucle for y actualiza la complejidad"""
        self.detalles_analisis['bucles_for'] += 1
        self.estructura_analizada.append(f"Bucle FOR (nivel {nivel_actual})")
        
        if nivel_actual > 0:
            self.detalles_analisis['bucles_anidados'] += 1
        
        self.detalles_analisis['nivel_anidamiento'] = max(
            self.detalles_analisis['nivel_anidamiento'], nivel_actual + 1
        )
        
        # Calcular OE por iteración
        oe_iteracion = 1  # Comparación
        for child in node.body:
            oe_iteracion += self._contar_oe_nodo(child)
        oe_iteracion += 2  # Incremento (i++ es 2 OE)
        
        self.detalles_analisis['oe_por_iteracion'] = oe_iteracion
        
        # Procesar cuerpo del bucle
        for child in node.body:
            self._visitar_nodos(child, nivel_actual + 1)
    def _calcular_tiempo_while(self, node):
        """
        Aplica el método específico para calcular tiempo en bucles while con división
        como en el ejemplo proporcionado: L ← L div 3 → O(log n)
        """
        # Paso 1: Identificar patrón de división/multiplicación en el cuerpo del while
        divisor = self._detectar_division_en_while(node)
        
        if divisor:
            # Caso logarítmico (como en tu ejemplo)
            # T(n) = (Log₃N + c)*4 + 2 = 4Log₃N + 4c + 2 → O(log n)
            base_log = divisor
            operaciones_ciclo = 4  # t=1 (condición) + t=2 (asignación) + t=1 (comparación)
            operaciones_base = 2   # Operaciones fuera del ciclo
            
            self.funcion_tiempo = f"T(n) = {operaciones_base} + {operaciones_ciclo}*log_{base_log}(n)"
            self.complejidad_detectada = f"O(log {base_log} n)"
            self.detalles_analisis['tipo_bucle'] = f"while con división por {base_log}"
            
        else:
            # Caso while lineal (análisis tradicional)
            oe_cuerpo = sum(self._contar_oe_nodo(n) for n in node.body)
            oe_condicion = 1  # 1 OE por evaluar la condición
            max_iteraciones = "n"  # No podemos determinar el límite, asumimos peor caso
            
            self.funcion_tiempo = f"T(n) = {oe_condicion} + {max_iteraciones}*({oe_cuerpo} + {oe_condicion})"
            self.complejidad_detectada = "O(n)"
            self.detalles_analisis['tipo_bucle'] = "while lineal"

    def _detectar_division_en_while(self, node):
        """
        Detecta si el while sigue el patrón: L ← L div k
        Retorna el divisor (k) si se encuentra, o None si no
        """
        for nodo in node.body:
            # Buscar asignaciones con división
            if isinstance(nodo, ast.AugAssign) and isinstance(nodo.op, ast.FloorDiv):
                if isinstance(nodo.target, ast.Name) and isinstance(nodo.value, ast.Constant):
                    return nodo.value.value
            
            if isinstance(nodo, ast.Assign):
                for target in nodo.targets:
                    if (isinstance(target, ast.Name) and 
                        isinstance(nodo.value, ast.BinOp) and 
                        isinstance(nodo.value.op, ast.FloorDiv)):
                        
                        if (isinstance(nodo.value.left, ast.Name) and \
                        nodo.value.left.id == target.id and \
                        isinstance(nodo.value.right, ast.Constant)):
                            return nodo.value.right.value
        
        return None
    def _procesar_bucle_while(self, nodo_while, nivel_actual):
        """Procesa un bucle while y actualiza la complejidad"""
        try:
            # Realizar el análisis
            resultados = self.analizador_while.analizar(nodo_while)
            
            # Actualizar resultados
            self.complejidad_detectada = resultados.get('complejidad', 'O(n)')
            self.funcion_tiempo = resultados.get('funcion_tiempo', 'T(n) = n * (OE por iteración)')
            
            # Actualizar detalles de análisis
            self.detalles_analisis.update({
                'bucles_while': self.detalles_analisis.get('bucles_while', 0) + 1,
                'tipo_bucle': resultados.get('tipo', 'while estándar'),
                'oe_cuerpo': resultados.get('oe_cuerpo', 1),
                'oe_por_iteracion': resultados.get('oe_por_iteracion', 1),
                'variables_control': resultados.get('variables_control', [])
            })
            
            # Registrar estructura
            self.estructura_analizada.append(f"Bucle WHILE ({resultados.get('tipo', 'while estándar')})")
            
        except Exception as e:
            print(f"Error al analizar bucle while: {str(e)}")
            # Valores por defecto en caso de error
            self.complejidad_detectada = "O(n)"
            self.funcion_tiempo = "T(n) = n * (OE por iteración)"
            self.detalles_analisis.update({
                'bucles_while': self.detalles_analisis.get('bucles_while', 0) + 1,
                'tipo_bucle': 'while (error en análisis)',
                'oe_cuerpo': 1,
                'oe_por_iteracion': 1,
                'variables_control': []
            })
    
    def _procesar_condicional(self, node, nivel_actual):
        """Procesa un condicional if"""
        self.detalles_analisis['condicionales'] += 1
        self.detalles_analisis['operaciones_primitivas'] += 1  # 1 OE por la condición
        self.estructura_analizada.append(f"Condicional IF (nivel {nivel_actual})")
        
        # Procesar cuerpo y else
        for child in node.body:
            self._visitar_nodos(child, nivel_actual)
        for child in node.orelse:
            self._visitar_nodos(child, nivel_actual)
    
    def _contar_oe_nodo(self, node):
        """Cuenta las OE en un nodo AST"""
        oe = 0
        if isinstance(node, ast.Assign):
            oe += 1
        elif isinstance(node, ast.AugAssign):
            oe += 2
        elif isinstance(node, ast.BinOp):
            oe += 1
        elif isinstance(node, ast.Compare):
            oe += len(node.ops)
        elif isinstance(node, ast.Call):
            oe += 1
            
        for child in ast.iter_child_nodes(node):
            oe += self._contar_oe_nodo(child)
            
        return oe
    
    def _determinar_complejidad(self):
        """
        Determina la complejidad temporal basada en las estructuras encontradas,
        siguiendo la jerarquía de complejidades.
        """
        # Primero determinamos el tipo de complejidad basado en las estructuras
        complejidad = "O(1)"
        
        if self.detalles_analisis['bucles_for'] > 0 or self.detalles_analisis['bucles_while'] > 0:
            # Verificar si hay bucles anidados
            if self.detalles_analisis['nivel_anidamiento'] >= 3:
                complejidad = f"O(n^{self.detalles_analisis['nivel_anidamiento']})"
            elif self.detalles_analisis['nivel_anidamiento'] == 2:
                complejidad = "O(n²)"
            else:
                # Verificar si es logarítmico (busqueda binaria, etc.)
                if self._es_complejidad_logaritmica():
                    complejidad = "O(log n)"
                else:
                    complejidad = "O(n)"
        
        # Si hay recursión, podría ser exponencial o factorial
        if self._tiene_recursion():
            complejidad = "O(2^n)"  # Asumimos exponencial por defecto
        
        self.complejidad_detectada = complejidad
    
    def _calcular_funcion_tiempo(self):
        """Calcula la función de tiempo T(n) basada en el análisis"""
        try:
            oe_fuera = str(self.detalles_analisis['operaciones_primitivas'] - self.detalles_analisis['oe_por_iteracion'])
            oe_iteracion = str(self.detalles_analisis['oe_por_iteracion'])
            
            if self.complejidad_detectada == "O(1)":
                self.funcion_tiempo = f"T(n) = {self.detalles_analisis['operaciones_primitivas']}"
            
            elif self.complejidad_detectada == "O(log n)":
                self.funcion_tiempo = f"T(n) = {oe_fuera} + {oe_iteracion}*log(n)"
            
            elif self.complejidad_detectada == "O(n)":
                self.funcion_tiempo = f"T(n) = {oe_fuera} + {oe_iteracion}*n"
            
            elif self.complejidad_detectada == "O(n log n)":
                self.funcion_tiempo = f"T(n) = {oe_fuera} + {oe_iteracion}*n*log(n)"
            
            elif self.complejidad_detectada == "O(n²)":
                self.funcion_tiempo = f"T(n) = {oe_fuera} + {oe_iteracion}*n²"
            
            elif self.complejidad_detectada == "O(n³)":
                self.funcion_tiempo = f"T(n) = {oe_fuera} + {oe_iteracion}*n³"
            
            elif self.complejidad_detectada.startswith("O(n^"):
                grado = self.complejidad_detectada.split("^")[1].replace(")", "")
                self.funcion_tiempo = f"T(n) = {oe_fuera} + {oe_iteracion}*n^{grado}"
            
            elif self.complejidad_detectada == "O(2^n)":
                self.funcion_tiempo = f"T(n) = {oe_fuera} + {oe_iteracion}*2^n"
            
            elif self.complejidad_detectada == "O(n!)":
                self.funcion_tiempo = f"T(n) = {oe_fuera} + {oe_iteracion}*n!"
            
            else:
                self.funcion_tiempo = "T(n) = Desconocido"
                
        except KeyError as e:
            self.funcion_tiempo = f"Error: Falta clave {str(e)} en detalles_analisis"
        except Exception as e:
            self.funcion_tiempo = f"Error al calcular T(n): {str(e)}"
    
    def _es_complejidad_logaritmica(self):
        """
        Intenta determinar si el algoritmo tiene complejidad logarítmica
        (por ejemplo, búsqueda binaria)
        """
        # Buscar patrones de división en bucles while
        for estructura in self.estructura_analizada:
            if "WHILE" in estructura and ("div" in estructura or "/" in estructura):
                return True
        return False
    
    def _tiene_recursion(self):
        """
        Detecta si el algoritmo usa recursión
        """
        # Buscar llamadas a la misma función
        for estructura in self.estructura_analizada:
            if "llamada recursiva" in estructura.lower():
                return True
        return False
    
    def obtener_resumen(self):
        """
        Retorna un resumen del análisis realizado
        """
        resumen = f"""
ANÁLISIS DE COMPLEJIDAD ALGORÍTMICA
=====================================

Complejidad detectada: {self.complejidad_detectada}
Función de tiempo estimada: {self.funcion_tiempo}

Detalles del análisis:
- Bucles FOR encontrados: {self.detalles_analisis['bucles_for']}
- Bucles WHILE encontrados: {self.detalles_analisis['bucles_while']}
- Bucles anidados: {self.detalles_analisis['bucles_anidados']}
- Nivel máximo de anidamiento: {self.detalles_analisis['nivel_anidamiento']}
- Operaciones primitivas: {self.detalles_analisis['operaciones_primitivas']}
- Condicionales: {self.detalles_analisis['condicionales']}
- Llamadas a funciones: {self.detalles_analisis['funciones']}
- OE por iteración en bucles: {self.detalles_analisis['oe_por_iteracion']}

Estructuras encontradas:
"""
        for estructura in self.estructura_analizada:
            resumen += f"- {estructura}\n"
            
        # Añadir explicación según el tipo de complejidad
        resumen += "\nEXPLICACIÓN DE LA FUNCIÓN DE TIEMPO:\n"
        if "O(1)" in self.complejidad_detectada:
            resumen += ("T(n) es constante porque no hay bucles que dependan del tamaño de entrada n. "
                       "El tiempo de ejecución no varía con la entrada.")
        elif "O(n)" in self.complejidad_detectada:
            resumen += ("T(n) es lineal porque contiene un bucle que se ejecuta n veces. "
                       f"Cada iteración del bucle realiza aproximadamente {self.detalles_analisis['oe_por_iteracion']} operaciones elementales.")
        elif "O(log n)" in self.complejidad_detectada:
            resumen += ("T(n) es logarítmico porque el tamaño del problema se reduce "
                       "en cada iteración (ej. división por un factor constante).")
        elif "O(n²)" in self.complejidad_detectada:
            resumen += ("T(n) es cuadrático porque contiene bucles anidados que se ejecutan "
                       "n*n veces. El tiempo crece con el cuadrado del tamaño de entrada.")
        elif "O(n^" in self.complejidad_detectada:
            grado = self.complejidad_detectada.split("^")[1].replace(")", "")
            resumen += (f"T(n) es polinomial de grado {grado} porque contiene {grado} "
                       "bucles anidados. El tiempo crece rápidamente con el tamaño de entrada.")
        elif "O(2^n)" in self.complejidad_detectada:
            resumen += ("T(n) es exponencial típicamente debido a recursión no optimizada. "
                       "El tiempo se duplica con cada incremento en el tamaño de entrada.")
            
        return resumen