import ast
from collections import Counter
import re

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
        self.codigo_fuente = ""
        self.lineas = []
        self.tree = None
        self.tiempo_algoritmo = TiempoAlgoritmo()
        self.estructura_analizada = []
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

    def analizar(self, codigo):
        self.codigo_fuente = codigo
        self.lineas = codigo.splitlines()
        self.tree = ast.parse(codigo)
        self._agregar_referencias_parent()
        self._procesar_nodos(self.tree)

    def _procesar_nodos(self, nodo):
        for child in ast.iter_child_nodes(nodo):
            if isinstance(child, ast.If):
                self._clasificar_if(child)
            elif isinstance(child, ast.For):
                self._clasificar_for(child)  # Lo analizamos aquí y NO recursamos más
            elif isinstance(child, ast.While):
                self._clasificar_while(child)
            else:
                # Procesar instrucciones simples
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

                # Seguir procesando hijos recursivamente
                self._procesar_nodos(child)

    def _visitar_nodos(self, nodo, nivel_actual):
        self._procesar_nodo(nodo, nivel_actual)
        for child in ast.iter_child_nodes(nodo):
            self._visitar_nodos(child, nivel_actual)

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
        # Lista para almacenar todos los bloques del condicional
        bloques = []
        
        # Procesar el bloque if principal
        bloques.append((self._extraer_codigo_bloque(nodo_if.body), "if"))
        
        # Procesar bloques elif
        current_node = nodo_if
        while current_node.orelse and any(isinstance(n, ast.If) for n in current_node.orelse):
            next_if = next(n for n in current_node.orelse if isinstance(n, ast.If))
            bloques.append((self._extraer_codigo_bloque(next_if.body), "elif"))
            current_node = next_if
        
        # Procesar bloque else (si existe)
        if current_node.orelse and not all(isinstance(n, ast.If) for n in current_node.orelse):
            bloques.append((self._extraer_codigo_bloque(current_node.orelse), "else"))
        
        # Analizar cada bloque por separado
        tiempos = []
        for codigo_bloque, tipo in bloques:
            analizador_temp = AnalizadorAlgoritmo()
            analizador_temp.analizar(codigo_bloque)
            tiempos.append(analizador_temp.tiempo_algoritmo)
        
        # Obtener el tiempo máximo de todos los bloques
        tiempo_max = self._obtener_tiempo_maximo(tiempos)
        
        # Sumar el tiempo máximo al contador principal
        self._sumar_tiempo(tiempo_max)
        
        # Clasificar el tipo de condicional
        bloque_completo = self._obtener_bloque(nodo_if)

        # Verifica si hay elif
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
        """Extrae el código fuente de un bloque de nodos AST y normaliza la indentación."""
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

        # Quitar la indentación mínima común a todas las líneas
        lineas_sin_indent = [linea[min_indent:] if len(linea) > min_indent else linea for linea in lineas_bloque]
        return "\n".join(lineas_sin_indent).strip()

    def _obtener_tiempo_maximo(self, tiempos):
        """Encuentra el tiempo algoritmo con la máxima complejidad"""
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
        """Suma los valores de un tiempo algoritmo al contador principal"""
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
        """Extrae el código fuente de una lista de nodos AST manteniendo la estructura"""
        if not nodos:
            return ""
        
        lineas = []
        # Encontrar la mínima indentación común
        min_indent = None
        
        for nodo in nodos:
            start_line = nodo.lineno - 1
            end_line = nodo.end_lineno if hasattr(nodo, 'end_lineno') else nodo.lineno
            
            # Asegurarse de no exceder los límites del archivo
            start_line = max(0, min(start_line, len(self.lineas)-1))
            end_line = max(0, min(end_line, len(self.lineas)))
            
            for i in range(start_line, end_line):
                linea = self.lineas[i]
                if linea.strip():  # Ignorar líneas vacías
                    current_indent = len(linea) - len(linea.lstrip())
                    if min_indent is None or current_indent < min_indent:
                        min_indent = current_indent
                    lineas.append(linea)
        
        # Si no hay líneas con contenido, retornar string vacío
        if not lineas:
            return ""
        
        # Quitar la indentación común mínima
        lineas_sin_indent = []
        for linea in lineas:
            if linea.strip():  # Solo procesar líneas no vacías
                if len(linea) > min_indent:
                    lineas_sin_indent.append(linea[min_indent:])
                else:
                    lineas_sin_indent.append(linea)
        
        return '\n'.join(lineas_sin_indent)

    def _clasificar_for(self, nodo):
        bloque = self._extraer_codigo_nodos([nodo])  # Extrae solo este for y su cuerpo

        # Analizar el cuerpo del for
        analizador_cuerpo = AnalizadorAlgoritmo()
        cuerpo_codigo = self._extraer_codigo_nodos(nodo.body)
        analizador_cuerpo.analizar(cuerpo_codigo)

        # Determinar si el for es lineal
        es_lineal = self._es_for_lineal(nodo)

        # Calcular nivel de anidamiento
        nivel = self._calcular_nivel_anidamiento(nodo)
        bloque_con_nivel = f"# Nivel de anidamiento: {nivel}\n{bloque}"

        if nivel > 1:
            self.instruccion_for_anidados.append(bloque_con_nivel)

            # Inicialización del for externo
            self.tiempo_algoritmo.agregar_constante()
            self.tiempo_algoritmo.cant_lineal += 3  # n*(1 comparación + 2 incremento)
            self.tiempo_algoritmo.cant_lineal += 1  # Inicialización for interno (ejecutado n veces)
            self.tiempo_algoritmo.cant_cuadratica += 3  # n²*(1 comparación + 2 incremento)

            # Cuerpo interno
            if analizador_cuerpo.tiempo_algoritmo.cant_constante > 0:
                self.tiempo_algoritmo.cant_cuadratica += analizador_cuerpo.tiempo_algoritmo.cant_constante
            if analizador_cuerpo.tiempo_algoritmo.cant_lineal > 0:
                self.tiempo_algoritmo.cant_cubica += analizador_cuerpo.tiempo_algoritmo.cant_lineal
        else:
            self.instruccion_for.append(bloque_con_nivel)

            # Inicialización
            self.tiempo_algoritmo.agregar_constante()
            self.tiempo_algoritmo.agregar_constante()

            if es_lineal:
                self.tiempo_algoritmo.cant_lineal += 3  # comparación, incremento
                self.tiempo_algoritmo.cant_lineal += analizador_cuerpo.tiempo_algoritmo.cant_constante
                self.tiempo_algoritmo.cant_cuadratica += analizador_cuerpo.tiempo_algoritmo.cant_lineal
            else:
                # For de rango constante
                self.tiempo_algoritmo.agregar_constante()
                self.tiempo_algoritmo.agregar_constante()
                self._sumar_tiempos(self.tiempo_algoritmo, analizador_cuerpo.tiempo_algoritmo)

    def _calcular_nivel_anidamiento(self, nodo):
        nivel = 0
        actual = nodo
        while hasattr(actual, 'parent'):
            if isinstance(actual.parent, ast.For):
                nivel += 1
            actual = actual.parent
        return nivel + 1  # Incluir el for actual
    
    def _es_for_lineal(self, nodo_for):
        """Determina si un for es lineal (range(n)) o constante (range(10))"""
        if isinstance(nodo_for.iter, ast.Call) and \
        isinstance(nodo_for.iter.func, ast.Name) and \
        nodo_for.iter.func.id == 'range':
            
            if len(nodo_for.iter.args) == 1:
                arg = nodo_for.iter.args[0]
                if isinstance(arg, ast.Name):
                    return True  # range(n) - lineal
                elif isinstance(arg, ast.Constant) and isinstance(arg.value, int):
                    return False  # range(10) - constante
        return True  # Por defecto asumimos lineal
    
    def _calcular_nivel_anidamiento(self, nodo_objetivo):
        # Paso 1: Agregar referencia al padre en todos los nodos
        for parent in ast.walk(self.tree):
            for child in ast.iter_child_nodes(parent):
                setattr(child, 'parent', parent)

        # Paso 2: Contar cuántos padres 'for' hay hasta la raíz
        nivel = 0
        actual = nodo_objetivo
        while hasattr(actual, 'parent'):
            actual = actual.parent
            if isinstance(actual, ast.For):
                nivel += 1

        return nivel + 1  # +1 porque el for actual es nivel 1

        
    def _sumar_tiempo_lineal(self, tiempo):
        """Convierte tiempo constante a lineal (multiplica por n)"""
        self.tiempo_algoritmo.cant_lineal += tiempo.cant_constante
        self.tiempo_algoritmo.cant_lineal += tiempo.cant_lineal
        self.tiempo_algoritmo.cant_cuadratica += tiempo.cant_cuadratica
        self.tiempo_algoritmo.cant_cubica += tiempo.cant_cubica

    def _sumar_tiempo_cuadratico(self, tiempo):
        """Convierte tiempo a cuadrático (constante->cuadrático, lineal->cúbico)"""
        self.tiempo_algoritmo.cant_cuadratica += tiempo.cant_constante
        self.tiempo_algoritmo.cant_cubica += tiempo.cant_lineal
        # Los términos cuadráticos y cúbicos se mantienen igual

    def _sumar_tiempo_cubico(self, tiempo):
        """Convierte tiempo a cúbico (constante->cúbico)"""
        self.tiempo_algoritmo.cant_cubica += tiempo.cant_constante
        # Los términos lineales y superiores se mantienen igual

    def _sumar_tiempos(self, tiempo_destino, tiempo_origen):
        """Suma los tiempos de dos objetos TiempoAlgoritmo y los asigna al destino"""
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
            print("DEBUG bloque_for_anidado:\n", bloque)  # <- elimina después de probar
            match = patron_nivel.search(bloque)
            if match:
                nivel = int(match.group(1))
                niveles_for.append(nivel)
            else:
                print("No se detectó el nivel en bloque:\n", bloque)  # <- debug temporal

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


# ============ EJEMPLO DE PRUEBA =============
if __name__ == "__main__":
    codigo = """
for i in range(n):
    for j in range(n):
        print(i)
        for k in range(n):
            print(j)
"""

    analizador = AnalizadorAlgoritmo()
    analizador.analizar(codigo)
    analizador.mostrar_resultados()
