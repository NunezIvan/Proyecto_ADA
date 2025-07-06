# analizador_while.py (corregido)
import ast
import math

class AnalizadorWhile:
    def __init__(self):
        self.resultados = {}

    def analizar(self, nodo_while):
        if not isinstance(nodo_while, ast.While):
            raise ValueError("Se esperaba un nodo While")

        self.resultados = {
            'tipo': 'while estándar',
            'oe_condicion': 0,
            'oe_cuerpo': 0,
            'oe_por_iteracion': 0,
            'iteraciones': 'n',
            'funcion_tiempo': '',
            'complejidad': 'O(n)',
            'variables_control': []
        }

        self.resultados['oe_condicion'] = self._contar_oe(nodo_while.test)

        base_log = self._detectar_cambio_logaritmico(nodo_while.body)

        self.resultados['oe_cuerpo'] = self._contar_oe_cuerpo(nodo_while.body)
        self.resultados['oe_por_iteracion'] = self.resultados['oe_condicion'] + self.resultados['oe_cuerpo']

        if base_log:
            self._configurar_caso_logaritmico(base_log)
        elif self._es_iteracion_fija(nodo_while):
            self._configurar_caso_constante()
        else:
            self._configurar_caso_lineal()

        return self.resultados

    def _detectar_cambio_logaritmico(self, cuerpo):
        for nodo in cuerpo:
            if isinstance(nodo, ast.Assign) and isinstance(nodo.value, ast.BinOp):
                var = nodo.targets[0].id if isinstance(nodo.targets[0], ast.Name) else None
                if isinstance(nodo.value.left, ast.Name) and nodo.value.left.id == var:
                    if isinstance(nodo.value.op, (ast.FloorDiv, ast.Mult)) and isinstance(nodo.value.right, ast.Constant):
                        self.resultados['variables_control'].append(var)
                        return nodo.value.right.value
        return None

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

    def _contar_oe_cuerpo(self, cuerpo):
        return sum(self._contar_oe(nodo) for nodo in cuerpo)

    def _es_iteracion_fija(self, nodo):
        if isinstance(nodo.test, ast.Compare):
            for comp in nodo.test.comparators:
                if isinstance(comp, ast.Constant):
                    return True
        return False

    def _configurar_caso_logaritmico(self, base):
        self.resultados.update({
            'tipo': f'while con multiplicación/división por {base}',
            'iteraciones': f'log_{base}(n)',
            'funcion_tiempo': f'T(n) = {self.resultados["oe_por_iteracion"]}*log_{base}(n) + c',
            'complejidad': f'O(log {base} n)'
        })

    def _configurar_caso_lineal(self):
        self.resultados.update({
            'tipo': 'while lineal',
            'iteraciones': 'n',
            'funcion_tiempo': f'T(n) = {self.resultados["oe_por_iteracion"]}*n + c',
            'complejidad': 'O(n)'
        })

    def _configurar_caso_constante(self):
        self.resultados.update({
            'tipo': 'while constante',
            'iteraciones': '10',
            'funcion_tiempo': f'T(n) = {self.resultados["oe_por_iteracion"]}*10 + c',
            'complejidad': 'O(1)'
        })
