import ast
import math

class AnalizadorWhile:
    def __init__(self):
        self.resultados = {
            'tipo': 'while estándar',
            'oe_condicion': 0,
            'oe_cuerpo': 0,
            'oe_por_iteracion': 0,
            'iteraciones': 'n',
            'funcion_tiempo': '',
            'complejidad': 'O(n)',
            'variables_control': [],
            # Añadidos para compatibilidad con AnalizadorAlgoritmo
            'oe_cuerpo': 0,
            'oe_por_iteracion': 0
        }

    def analizar(self, nodo_while):
        """Analiza el bucle while y su cuerpo completo"""
        if not isinstance(nodo_while, ast.While):
            raise ValueError("Se esperaba un nodo While")

        # Reiniciar resultados
        self.resultados = {
            'tipo': 'while estándar',
            'oe_condicion': 0,
            'oe_cuerpo': 0,
            'oe_por_iteracion': 0,
            'iteraciones': 'n',
            'funcion_tiempo': '',
            'complejidad': 'O(n)',
            'variables_control': [],
            'oe_cuerpo': 0,
            'oe_por_iteracion': 0
        }

        # 1. Analizar la condición del while
        self.resultados['oe_condicion'] = self._contar_oe(nodo_while.test)

        # 2. Detectar patrón logarítmico (división/multiplicación)
        divisor = self._detectar_division_logaritmica(nodo_while.body)

        # 3. Contar OE en el cuerpo (todas las instrucciones)
        self.resultados['oe_cuerpo'] = self._contar_oe_cuerpo(nodo_while.body)

        # 4. Calcular OE por iteración
        self.resultados['oe_por_iteracion'] = self.resultados['oe_condicion'] + self.resultados['oe_cuerpo']

        # 5. Determinar tipo de bucle
        if divisor:
            self._configurar_caso_logaritmico(divisor)
        else:
            self._configurar_caso_lineal()

        # Retornar los resultados para mayor compatibilidad
        return self.resultados

    def _detectar_division_logaritmica(self, cuerpo):
        """Detecta asignaciones como L = L // k o L = L * k"""
        for nodo in cuerpo:
            if isinstance(nodo, ast.Assign) and \
               isinstance(nodo.value, ast.BinOp) and \
               isinstance(nodo.targets[0], ast.Name):
                
                var = nodo.targets[0].id
                if isinstance(nodo.value.left, ast.Name) and nodo.value.left.id == var:
                    if isinstance(nodo.value.op, ast.FloorDiv):
                        if isinstance(nodo.value.right, ast.Constant):
                            self.resultados['variables_control'].append(var)
                            return nodo.value.right.value
        return None

    def _contar_oe_cuerpo(self, cuerpo):
        """Cuenta todas las OE en el cuerpo del while"""
        return sum(self._contar_oe(nodo) for nodo in cuerpo)

    def _contar_oe(self, nodo):
        """Cuenta OE en un nodo específico"""
        if isinstance(nodo, ast.Assign):
            return 1 + self._contar_oe(nodo.value)
        elif isinstance(nodo, ast.BinOp):
            return 1 + self._contar_oe(nodo.left) + self._contar_oe(nodo.right)
        elif isinstance(nodo, ast.Compare):
            return 1 + sum(self._contar_oe(comp) for comp in nodo.comparators)
        elif isinstance(nodo, ast.Call):
            return 1 + sum(self._contar_oe(arg) for arg in nodo.args)
        elif isinstance(nodo, ast.Constant):
            return 0
        return 1  # Para otros nodos no contabilizados

    def _configurar_caso_logaritmico(self, divisor):
        """Configura para el caso logarítmico O(log_k n)"""
        self.resultados.update({
            'tipo': f'while con división por {divisor}',
            'iteraciones': f'log_{divisor}(n) + c',
            'funcion_tiempo': f'T(n) = {self.resultados["oe_por_iteracion"]}*(log_{divisor}(n) + c) + 2',
            'complejidad': f'O(log {divisor} n)'
        })

    def _configurar_caso_lineal(self):
        """Configura para el caso lineal O(n)"""
        self.resultados.update({
            'tipo': 'while lineal',
            'iteraciones': 'n',
            'funcion_tiempo': f'T(n) = {self.resultados["oe_por_iteracion"]}*n + c',
            'complejidad': 'O(n)'
        })