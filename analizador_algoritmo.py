# analizador_algoritmo.py (versión completa integrada)
import ast
from collections import Counter
import re
from tkinter import messagebox
import math

class TiempoAlgoritmo:
    def __init__(self):
        self.cant_constante = 0
        self.cant_lineal = 0
        self.cant_cuadratica = 0
        self.cant_cubica = 0
        self.cant_nlogn = 0
        self.log_bases = {base: 0 for base in range(2, 11)}

    def agregar_constante(self):
        self.cant_constante += 1

    def agregar_lineal(self):
        self.cant_lineal += 1

    def agregar_cuadratica(self):
        self.cant_cuadratica += 1

    def agregar_cubica(self):
        self.cant_cubica += 1

    def agregar_nlogn(self):
        self.cant_nlogn += 1

    def agregar_logaritmica_base(self, base):
        if base in self.log_bases:
            self.log_bases[base] += 1


class AnalizadorAlgoritmo:
    def __init__(self):
        # Variables del análisis original
        self.codigo_fuente = ""
        self.estructura_analizada = []
        self.complejidad_detectada = "O(1)"
        self.funcion_tiempo = ""
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
        
        # Variables del nuevo sistema de análisis
        self.lineas = []
        self.tree = None
        self.tiempo_algoritmo = TiempoAlgoritmo()
        
        self.instruccion_simples = []
        self.instruccion_simples_aumentadas = []
        self.instruccion_compuesta = []

        self.instruccion_condicionales = []                  # if
        self.instruccion_condicionales_completas = []        # if-else
        self.instruccion_condicionales_compuestas = []       # if-elif
        self.instruccion_condicionales_compuestas_completas = []  # if-elif-else

        self.instruccion_for = []
        self.instruccion_for_anidados = []
        self.instruccion_for_conwhile = []

        self.instruccion_while = []
        self.instruccion_while_anidados = []
        self.instruccion_while_confor = []

    def analizar_codigo(self, codigo):
        self.codigo_fuente = codigo
        self._reset_analisis()

        try:
            self.tree = ast.parse(codigo)
            self.lineas = codigo.splitlines()
            self._agregar_referencias_parent()
            
            # Realizar ambos tipos de análisis
            self._visitar_nodos(self.tree, 0)
            self._procesar_nodos(self.tree)
            
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
        
        # Resetear también las variables del nuevo sistema
        self.tiempo_algoritmo = TiempoAlgoritmo()
        self.instruccion_simples = []
        self.instruccion_simples_aumentadas = []
        self.instruccion_compuesta = []
        self.instruccion_condicionales = []
        self.instruccion_condicionales_completas = []
        self.instruccion_condicionales_compuestas = []
        self.instruccion_condicionales_compuestas_completas = []
        self.instruccion_for = []
        self.instruccion_for_anidados = []
        self.instruccion_for_conwhile = []
        self.instruccion_while = []
        self.instruccion_while_anidados = []
        self.instruccion_while_confor = []

    def _visitar_nodos(self, node, nivel_actual):
        self._procesar_nodo(node, nivel_actual)
        for child in ast.iter_child_nodes(node):
            self._visitar_nodos(child, nivel_actual)

    def _procesar_nodo(self, node, nivel_actual):
        if isinstance(node, ast.FunctionDef):
            return

        if isinstance(node, ast.Assign) or isinstance(node, ast.AugAssign):
            self.detalles_analisis['operaciones_primitivas'] += self._contar_oe(node)
        elif isinstance(node, ast.BinOp) or isinstance(node, ast.Compare) or isinstance(node, ast.Call):
            self.detalles_analisis['operaciones_primitivas'] += self._contar_oe(node)

        if isinstance(node, ast.For):
            self._procesar_bucle_for(node, nivel_actual)
        elif isinstance(node, ast.While):
            self._procesar_bucle_while(node, nivel_actual)
        elif isinstance(node, ast.If):
            self._procesar_condicional(node, nivel_actual)

    def _procesar_bucle_for(self, node, nivel_actual):
        self.detalles_analisis['bucles_for'] += 1
        self.estructura_analizada.append(f"Bucle FOR (nivel {nivel_actual})")

        if nivel_actual > 0:
            self.detalles_analisis['bucles_anidados'] += 1

        self.detalles_analisis['nivel_anidamiento'] = max(
            self.detalles_analisis['nivel_anidamiento'], nivel_actual + 1
        )

        oe_iteracion = sum(self._contar_oe(child) for child in node.body)
        self.detalles_analisis['oe_por_iteracion'] += oe_iteracion + 1  # 1 comparación por vuelta

        for child in node.body:
            self._visitar_nodos(child, nivel_actual + 1)

    def _procesar_bucle_while(self, node, nivel_actual):
        self.detalles_analisis['bucles_while'] += 1
        self.estructura_analizada.append(f"Bucle WHILE (nivel {nivel_actual})")
        
        if nivel_actual > 0:
            self.detalles_analisis['bucles_anidados'] += 1

        self.detalles_analisis['nivel_anidamiento'] = max(
            self.detalles_analisis['nivel_anidamiento'], nivel_actual + 1
        )

        oe_iteracion = sum(self._contar_oe(child) for child in node.body)
        self.detalles_analisis['oe_por_iteracion'] += oe_iteracion + 1  # 1 comparación por vuelta

        for child in node.body:
            self._visitar_nodos(child, nivel_actual + 1)

    def _procesar_condicional(self, node, nivel_actual):
        self.detalles_analisis['condicionales'] += 1
        self.detalles_analisis['operaciones_primitivas'] += 1
        self.estructura_analizada.append(f"Condicional IF (nivel {nivel_actual})")

        for child in node.body:
            self._visitar_nodos(child, nivel_actual)
        for child in node.orelse:
            self._visitar_nodos(child, nivel_actual)

    def _contar_oe(self, nodo):
        if isinstance(nodo, ast.FunctionDef) or isinstance(nodo, ast.Subscript):
            return 0
        if isinstance(nodo, ast.Assign):
            return 1 + self._contar_oe(nodo.value)
        elif isinstance(nodo, ast.AugAssign):
            return 2 + self._contar_oe(nodo.value)
        elif isinstance(nodo, ast.BinOp):
            return 1 + self._contar_oe(nodo.left) + self._contar_oe(nodo.right)
        elif isinstance(nodo, ast.Compare):
            return 1 + sum(self._contar_oe(comp) for comp in nodo.comparators)
        elif isinstance(nodo, ast.Call):
            return 1 + sum(self._contar_oe(arg) for arg in nodo.args)
        elif isinstance(nodo, ast.Constant):
            return 0
        else:
            return sum(self._contar_oe(child) for child in ast.iter_child_nodes(nodo))

    def _determinar_complejidad(self):
        # Primero verificar la complejidad basada en el tiempo de algoritmo
        if self.tiempo_algoritmo.cant_cubica > 0:
            self.complejidad_detectada = "O(n^3)"
        elif self.tiempo_algoritmo.cant_cuadratica > 0:
            self.complejidad_detectada = "O(n²)"
        elif self.tiempo_algoritmo.cant_nlogn > 0:
            self.complejidad_detectada = "O(n log n)"
        elif self.tiempo_algoritmo.cant_lineal > 0:
            self.complejidad_detectada = "O(n)"
        elif any(count > 0 for count in self.tiempo_algoritmo.log_bases.values()):
            # Tomar la primera base de logaritmo con conteo > 0
            base = next(b for b, cnt in self.tiempo_algoritmo.log_bases.items() if cnt > 0)
            self.complejidad_detectada = f"O(log_{base} n)"
        else:
            self.complejidad_detectada = "O(1)"

    def _calcular_funcion_tiempo(self):
        try:
            # Calcular basado en el tiempo de algoritmo
            partes = []
            
            if self.tiempo_algoritmo.cant_cubica > 0:
                partes.append(f"{self.tiempo_algoritmo.cant_cubica}n³")
            if self.tiempo_algoritmo.cant_cuadratica > 0:
                partes.append(f"{self.tiempo_algoritmo.cant_cuadratica}n²")
            if self.tiempo_algoritmo.cant_nlogn > 0:
                partes.append(f"{self.tiempo_algoritmo.cant_nlogn}n log n")
            if self.tiempo_algoritmo.cant_lineal > 0:
                partes.append(f"{self.tiempo_algoritmo.cant_lineal}n")
                
            # Agregar términos logarítmicos
            for base, count in self.tiempo_algoritmo.log_bases.items():
                if count > 0:
                    partes.append(f"{count}log_{base}(n)")
                    
            if self.tiempo_algoritmo.cant_constante > 0:
                partes.append(str(self.tiempo_algoritmo.cant_constante))
                
            if not partes:
                self.funcion_tiempo = "T(n) = 1"
            else:
                self.funcion_tiempo = "T(n) = " + " + ".join(partes)
                
        except Exception as e:
            self.funcion_tiempo = f"Error al calcular T(n): {str(e)}"

    # ===== Métodos del nuevo sistema de análisis =====
    def _procesar_nodos(self, nodo):
        for child in ast.iter_child_nodes(nodo):
            if isinstance(child, ast.If):
                self._clasificar_if(child)
            elif isinstance(child, ast.For):
                self._clasificar_for(child)
            elif isinstance(child, ast.While):
                self._clasificar_while(child)
            else:
                if isinstance(child, ast.Assign):
                    self._procesar_instruccion_simple(child)
                elif isinstance(child, ast.AugAssign):
                    self._procesar_instruccion_aumentada(child)
                elif isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
                    if isinstance(child.value.func, ast.Name) and child.value.func.id == 'print':
                        self._procesar_print(child)
                    else:
                        self._procesar_instruccion_simple(child)
                elif isinstance(child, ast.Return):
                    self._procesar_return(child)
                elif isinstance(child, ast.Compare):
                    self._procesar_comparacion(child)

                self._procesar_nodos(child)

    def _procesar_instruccion_simple(self, nodo):
        lineno = nodo.lineno
        self.instruccion_simples.append(self.lineas[lineno - 1].strip())
        self.tiempo_algoritmo.agregar_constante()

    def _procesar_print(self, nodo):
        lineno = nodo.lineno
        self.instruccion_simples.append(self.lineas[lineno - 1].strip())
        self.tiempo_algoritmo.agregar_constante()

    def _procesar_return(self, nodo):
        lineno = nodo.lineno
        self.instruccion_simples.append(self.lineas[lineno - 1].strip())
        self.tiempo_algoritmo.agregar_constante()

    def _procesar_comparacion(self, nodo):
        lineno = nodo.lineno
        comparacion = self.lineas[lineno - 1].strip()
        ops = nodo.ops

        if any(isinstance(op, (ast.Gt, ast.Lt, ast.Eq)) for op in ops):
            self.instruccion_simples.append(comparacion)
            self.tiempo_algoritmo.agregar_constante()
        elif any(isinstance(op, (ast.GtE, ast.LtE, ast.NotEq)) for op in ops):
            self.instruccion_compuestas.append(comparacion)
            self.tiempo_algoritmo.agregar_constante()
            self.tiempo_algoritmo.agregar_constante()

    def _procesar_instruccion_aumentada(self, nodo):
        lineno = nodo.lineno
        self.instruccion_simples_aumentadas.append(self.lineas[lineno - 1].strip())
        self.tiempo_algoritmo.agregar_constante()
        self.tiempo_algoritmo.agregar_constante()

    def _obtener_bloque(self, nodo):
        start_line = nodo.lineno - 1
        end_line = self._encontrar_fin_bloque(start_line)
        return "\n".join(self.lineas[start_line:end_line])

    def _clasificar_if(self, nodo_if):
        bloques = []
        bloques.append((self._extraer_codigo_bloque(nodo_if.body), "if"))
        
        current_node = nodo_if
        while current_node.orelse and any(isinstance(n, ast.If) for n in current_node.orelse):
            next_if = next(n for n in current_node.orelse if isinstance(n, ast.If))
            bloques.append((self._extraer_codigo_bloque(next_if.body), "elif"))
            current_node = next_if
        
        if current_node.orelse and not all(isinstance(n, ast.If) for n in current_node.orelse):
            bloques.append((self._extraer_codigo_bloque(current_node.orelse), "else"))
        
        tiempos = []
        for codigo_bloque, tipo in bloques:
            analizador_temp = AnalizadorAlgoritmo()
            analizador_temp.analizar_codigo(codigo_bloque)
            tiempos.append(analizador_temp.tiempo_algoritmo)
        
        tiempo_max = self._obtener_tiempo_maximo(tiempos)
        self._sumar_tiempo(tiempo_max)
        
        bloque_completo = self._obtener_bloque(nodo_if)
        hay_elif = False
        hay_else = False

        current = nodo_if
        while current.orelse:
            if all(isinstance(n, ast.If) for n in current.orelse):
                hay_elif = True
                current = current.orelse[0]
            else:
                hay_else = True
                break

        if hay_elif and hay_else:
            self.instruccion_condicionales_compuestas_completas.append(bloque_completo)
        elif hay_elif:
            self.instruccion_condicionales_compuestas.append(bloque_completo)
        elif hay_else:
            self.instruccion_condicionales_completas.append(bloque_completo)
        else:
            self.instruccion_condicionales.append(bloque_completo)

    def _extraer_codigo_bloque(self, nodos):
        if not nodos:
            return ""

        lineas_bloque = []
        min_indent = None

        for nodo in nodos:
            start = nodo.lineno - 1
            end = nodo.end_lineno if hasattr(nodo, 'end_lineno') else nodo.lineno
            for i in range(start, end):
                linea = self.lineas[i]
                if linea.strip() == "":
                    continue
                lineas_bloque.append(linea)
                indent_actual = len(linea) - len(linea.lstrip())
                if min_indent is None or indent_actual < min_indent:
                    min_indent = indent_actual

        lineas_sin_indent = [linea[min_indent:] if len(linea) > min_indent else linea for linea in lineas_bloque]
        return "\n".join(lineas_sin_indent).strip()

    def _obtener_tiempo_maximo(self, tiempos):
        max_tiempo = TiempoAlgoritmo()
        
        for tiempo in tiempos:
            if tiempo.cant_constante > max_tiempo.cant_constante:
                max_tiempo.cant_constante = tiempo.cant_constante
            if tiempo.cant_lineal > max_tiempo.cant_lineal:
                max_tiempo.cant_lineal = tiempo.cant_lineal
            if tiempo.cant_cuadratica > max_tiempo.cant_cuadratica:
                max_tiempo.cant_cuadratica = tiempo.cant_cuadratica
            if tiempo.cant_cubica > max_tiempo.cant_cubica:
                max_tiempo.cant_cubica = tiempo.cant_cubica
            if tiempo.cant_nlogn > max_tiempo.cant_nlogn:
                max_tiempo.cant_nlogn = tiempo.cant_nlogn
            
            for base in tiempo.log_bases:
                if tiempo.log_bases[base] > max_tiempo.log_bases[base]:
                    max_tiempo.log_bases[base] = tiempo.log_bases[base]
        
        return max_tiempo

    def _sumar_tiempo(self, tiempo):
        for _ in range(tiempo.cant_constante):
            self.tiempo_algoritmo.agregar_constante()
        for _ in range(tiempo.cant_lineal):
            self.tiempo_algoritmo.agregar_lineal()
        for _ in range(tiempo.cant_cuadratica):
            self.tiempo_algoritmo.agregar_cuadratica()
        for _ in range(tiempo.cant_cubica):
            self.tiempo_algoritmo.agregar_cubica()
        for _ in range(tiempo.cant_nlogn):
            self.tiempo_algoritmo.agregar_nlogn()
        
        for base in tiempo.log_bases:
            for _ in range(tiempo.log_bases[base]):
                self.tiempo_algoritmo.agregar_logaritmica_base(base)

    def _extraer_codigo_nodos(self, nodos):
        if not nodos:
            return ""
        
        lineas = []
        min_indent = None
        
        for nodo in nodos:
            start_line = nodo.lineno - 1
            end_line = nodo.end_lineno if hasattr(nodo, 'end_lineno') else nodo.lineno
            
            start_line = max(0, min(start_line, len(self.lineas)-1))
            end_line = max(0, min(end_line, len(self.lineas)))
            
            for i in range(start_line, end_line):
                linea = self.lineas[i]
                if linea.strip():
                    current_indent = len(linea) - len(linea.lstrip())
                    if min_indent is None or current_indent < min_indent:
                        min_indent = current_indent
                    lineas.append(linea)
        
        if not lineas:
            return ""
        
        lineas_sin_indent = []
        for linea in lineas:
            if linea.strip():
                if len(linea) > min_indent:
                    lineas_sin_indent.append(linea[min_indent:])
                else:
                    lineas_sin_indent.append(linea)
        
        return '\n'.join(lineas_sin_indent)

    def _clasificar_for(self, nodo):
        bloque = self._extraer_codigo_nodos([nodo])
        analizador_cuerpo = AnalizadorAlgoritmo()
        cuerpo_codigo = self._extraer_codigo_nodos(nodo.body)
        analizador_cuerpo.analizar_codigo(cuerpo_codigo)

        es_lineal = self._es_for_lineal(nodo)
        nivel = self._calcular_nivel_anidamiento(nodo)
        bloque_con_nivel = f"# Nivel de anidamiento: {nivel}\n{bloque}"

        if nivel > 1:
            self.instruccion_for_anidados.append(bloque_con_nivel)
            self.tiempo_algoritmo.agregar_constante()
            self.tiempo_algoritmo.cant_lineal += 3
            self.tiempo_algoritmo.cant_lineal += 1
            self.tiempo_algoritmo.cant_cuadratica += 3

            if analizador_cuerpo.tiempo_algoritmo.cant_constante > 0:
                self.tiempo_algoritmo.cant_cuadratica += analizador_cuerpo.tiempo_algoritmo.cant_constante
            if analizador_cuerpo.tiempo_algoritmo.cant_lineal > 0:
                self.tiempo_algoritmo.cant_cubica += analizador_cuerpo.tiempo_algoritmo.cant_lineal
        else:
            self.instruccion_for.append(bloque_con_nivel)
            self.tiempo_algoritmo.agregar_constante()
            self.tiempo_algoritmo.agregar_constante()

            if es_lineal:
                self.tiempo_algoritmo.cant_lineal += 3
                self.tiempo_algoritmo.cant_lineal += analizador_cuerpo.tiempo_algoritmo.cant_constante
                self.tiempo_algoritmo.cant_cuadratica += analizador_cuerpo.tiempo_algoritmo.cant_lineal
            else:
                self.tiempo_algoritmo.agregar_constante()
                self.tiempo_algoritmo.agregar_constante()
                self._sumar_tiempos(self.tiempo_algoritmo, analizador_cuerpo.tiempo_algoritmo)

    def _es_for_lineal(self, nodo_for):
        if isinstance(nodo_for.iter, ast.Call) and \
        isinstance(nodo_for.iter.func, ast.Name) and \
        nodo_for.iter.func.id == 'range':
            
            if len(nodo_for.iter.args) == 1:
                arg = nodo_for.iter.args[0]
                if isinstance(arg, ast.Name):
                    return True
                elif isinstance(arg, ast.Constant) and isinstance(arg.value, int):
                    return False
        return True
    
    def _calcular_nivel_anidamiento(self, nodo_objetivo):
        for parent in ast.walk(self.tree):
            for child in ast.iter_child_nodes(parent):
                setattr(child, 'parent', parent)

        nivel = 0
        actual = nodo_objetivo
        while hasattr(actual, 'parent'):
            actual = actual.parent
            if isinstance(actual, ast.For):
                nivel += 1

        return nivel + 1

    def _sumar_tiempos(self, tiempo_destino, tiempo_origen):
        tiempo_destino.cant_constante += tiempo_origen.cant_constante
        tiempo_destino.cant_lineal += tiempo_origen.cant_lineal
        tiempo_destino.cant_cuadratica += tiempo_origen.cant_cuadratica
        tiempo_destino.cant_cubica += tiempo_origen.cant_cubica
        tiempo_destino.cant_nlogn += tiempo_origen.cant_nlogn
        
        for base in tiempo_origen.log_bases:
            if base in tiempo_destino.log_bases:
                tiempo_destino.log_bases[base] += tiempo_origen.log_bases[base]

    def _clasificar_while(self, nodo):
        bloque = self._obtener_bloque(nodo)
        tiene_while = any(isinstance(n, ast.While) for n in ast.iter_child_nodes(nodo))
        tiene_for = any(isinstance(n, ast.For) for n in ast.iter_child_nodes(nodo))

        if tiene_while:
            self.instruccion_while_anidados.append(bloque)
        elif tiene_for:
            self.instruccion_while_confor.append(bloque)
        else:
            self.instruccion_while.append(bloque)

    def _encontrar_fin_bloque(self, start_index):
        base_indent = len(self.lineas[start_index]) - len(self.lineas[start_index].lstrip())
        for i in range(start_index + 1, len(self.lineas)):
            linea = self.lineas[i]
            if linea.strip() == "":
                continue
            indent = len(linea) - len(linea.lstrip())
            if indent <= base_indent:
                return i
        return len(self.lineas)

    def _agregar_referencias_parent(self):
        for nodo in ast.walk(self.tree):
            for hijo in ast.iter_child_nodes(nodo):
                hijo.parent = nodo

    def mostrar_resultados(self):
        def imprimir_bloques(nombre, bloques):
            print(f"\n--- {nombre.upper()} ({len(bloques)}) ---")
            for i, b in enumerate(bloques, 1):
                print(f"\n[{nombre} #{i}]:\n{b}")

        imprimir_bloques("Asignaciones simples", self.instruccion_simples)
        imprimir_bloques("Asignaciones aumentadas", self.instruccion_simples_aumentadas)

        imprimir_bloques("Condicional IF", self.instruccion_condicionales)
        imprimir_bloques("Condicional IF-ELSE", self.instruccion_condicionales_completas)
        imprimir_bloques("Condicional IF-ELIF", self.instruccion_condicionales_compuestas)
        imprimir_bloques("Condicional IF-ELIF-ELSE", self.instruccion_condicionales_compuestas_completas)

        imprimir_bloques("Bucles FOR", self.instruccion_for)
        imprimir_bloques("Bucles FOR anidados", self.instruccion_for_anidados)
        imprimir_bloques("Bucles FOR con WHILE", self.instruccion_for_conwhile)

        imprimir_bloques("Bucles WHILE", self.instruccion_while)
        imprimir_bloques("Bucles WHILE anidados", self.instruccion_while_anidados)
        imprimir_bloques("Bucles WHILE con FOR", self.instruccion_while_confor)

        niveles_for = []
        patron_nivel = re.compile(r"# Nivel de anidamiento: (\d+)")

        for bloque in self.instruccion_for_anidados:
            match = patron_nivel.search(bloque)
            if match:
                nivel = int(match.group(1))
                niveles_for.append(nivel)

        conteo_niveles = Counter(niveles_for)
        if conteo_niveles:
            print("\n--- RESUMEN DE NIVELES DE ANIDAMIENTO ---")
            for nivel, cantidad in sorted(conteo_niveles.items()):
                print(f"Bucle FOR con nivel {nivel}: {cantidad} encontrados")
        else:
            print("\n[!] No se detectaron niveles de anidamiento correctamente.")

        print("Cantidad de OEs (Operaciones Elementales Constantes):", self.tiempo_algoritmo.cant_constante)
        print("Cantidad de OEs (Operaciones Elementales Lineales):", self.tiempo_algoritmo.cant_lineal)
        print("Cantidad de OEs (Operaciones Elementales Cuadraticos):", self.tiempo_algoritmo.cant_cuadratica)
        print("Cantidad de OEs (Operaciones Elementales Cubicos):", self.tiempo_algoritmo.cant_cubica)

    def obtener_resumen(self):
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
- Condicionales: {self.detalles_analisis['condicionales']}
- Llamadas a funciones: {self.detalles_analisis['funciones']}

Estructuras encontradas:
"""
        for estructura in self.estructura_analizada:
            resumen += f"- {estructura}\n"
        
        resumen += "\nDETALLES DE COMPLEJIDAD:\n"
        resumen += f"- Operaciones constantes (O(1)): {self.tiempo_algoritmo.cant_constante}\n"
        resumen += f"- Operaciones lineales (O(n)): {self.tiempo_algoritmo.cant_lineal}\n"
        resumen += f"- Operaciones cuadráticas (O(n²)): {self.tiempo_algoritmo.cant_cuadratica}\n"
        resumen += f"- Operaciones cúbicas (O(n³)): {self.tiempo_algoritmo.cant_cubica}\n"
        resumen += f"- Operaciones O(n log n): {self.tiempo_algoritmo.cant_nlogn}\n"
        
        for base, count in self.tiempo_algoritmo.log_bases.items():
            if count > 0:
                resumen += f"- Operaciones logarítmicas (log_{base} n): {count}\n"
        
        return resumen


# Ejemplo de uso
if __name__ == "__main__":
    codigo = """
for i in range(n):
    for j in range(n):
        print(i)
        for k in range(n):
            print(j)
"""

    analizador = AnalizadorAlgoritmo()
    analizador.analizar_codigo(codigo)
    print(analizador.obtener_resumen())
    analizador.mostrar_resultados()