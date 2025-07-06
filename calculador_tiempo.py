# calculador_tiempo.py (versión final corregida con consistencia entre OE y T(n))
import re
import math
from tkinter import messagebox

class CalculadorTiempo:
    def __init__(self):
        self.contador_oe = 0
        self.lineas_analizadas = []
        self.funcion_tiempo = ""
        self.complejidad = "O(1)"
        self.bucles_for_detectados = []
        self.oe_por_iteracion = 0
        self.anidamiento_maximo = 0

    def analizar_codigo(self, codigo):
        self.contador_oe = 0
        self.lineas_analizadas = []
        self.funcion_tiempo = ""
        self.complejidad = "O(1)"
        self.bucles_for_detectados = []
        self.oe_por_iteracion = 0
        self.anidamiento_maximo = 0

        try:
            lineas = codigo.split('\n')
            for i, linea in enumerate(lineas):
                linea_original = linea
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue
                self._analizar_linea(linea, linea_original)

            self._determinar_funcion_tiempo()
            return self.contador_oe

        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el código: {str(e)}")
            return 0

    def _analizar_linea(self, linea, linea_original):
        oe_linea = 0

        if ':=' in linea or '=' in linea.split()[0]:
            oe_linea += self._contar_declaracion(linea)
        elif linea.startswith(('if ', 'elif ')):
            oe_linea += self._contar_condicional(linea)
        elif linea.startswith(('for ', 'while ')):
            indent = len(linea_original) - len(linea_original.lstrip(' '))
            self.bucles_for_detectados.append(indent)
            self.anidamiento_maximo = max(self.anidamiento_maximo, indent)
            oe_linea += self._contar_bucle(linea_original)
        elif '(' in linea and ')' in linea:
            oe_linea += self._contar_llamada_funcion(linea)
        else:
            oe_linea += self._contar_operaciones(linea)

        self.contador_oe += oe_linea
        self.lineas_analizadas.append(f"{linea} // OE: {oe_linea}")

    def _contar_declaracion(self, linea):
        if '=' in linea:
            partes = linea.split('=')
            return 1 + self._contar_operaciones(partes[1])
        return 0

    def _contar_condicional(self, linea):
        condicion = linea[linea.find('(')+1:linea.rfind(')')] if '(' in linea and ')' in linea else linea
        return 1 + self._contar_operaciones(condicion)

    def _contar_bucle(self, linea_original):
        linea = linea_original.strip()
        if linea.startswith('for'):
            return self._contar_for(linea)
        elif linea.startswith('while'):
            return self._contar_while(linea)
        return 0

    def _contar_for(self, linea):
        if ' in ' in linea:
            condition = linea.split(' in ')[1].strip()
            self.oe_por_iteracion += 1  # estimado fijo por iteración
            return 1 + self._contar_operaciones(condition)
        return 0

    def _contar_while(self, linea):
        condicion = linea[linea.find('(')+1:linea.rfind(')')] if '(' in linea and ')' in linea else linea
        self.oe_por_iteracion += 1
        return 1 + self._contar_operaciones(condicion)

    def _contar_llamada_funcion(self, linea):
        parametros = linea[linea.find('(')+1:linea.rfind(')')]
        return 1 + (self._contar_operaciones(parametros) if parametros else 0)

    def _contar_operaciones(self, expresion):
        if not expresion.strip():
            return 0

        operadores = r'\+|\-|\*|\/|\%|\*\*|\/\/|==|!=|<=|>=|<|>|and|or|not'
        matches = re.findall(operadores, expresion)
        oe = len(matches)

        for op in ['+=', '-=', '*=', '/=']:
            if op in expresion:
                oe += 1
                break

        indexaciones = re.findall(r'\w+\[.+?\]', expresion)
        oe -= len(indexaciones)

        return max(0, oe)

    def _determinar_funcion_tiempo(self):
        profundidad = self._calcular_nivel_anidamiento(self.bucles_for_detectados)

        if profundidad >= 2:
            self.complejidad = f"O(n^{profundidad})" if profundidad > 2 else "O(n²)"
            self.funcion_tiempo = f"T(n) = {self.oe_por_iteracion} * n^{profundidad} + c"
        elif profundidad == 1:
            self.complejidad = "O(n)"
            self.funcion_tiempo = f"T(n) = {self.oe_por_iteracion} * n + c"
        else:
            self.funcion_tiempo = f"T(n) = {self.contador_oe}"
            self.complejidad = "O(1)"

    def _calcular_nivel_anidamiento(self, indentaciones):
        indentaciones.sort()
        niveles = [0] * len(indentaciones)

        for i in range(1, len(indentaciones)):
            if indentaciones[i] > indentaciones[i - 1]:
                niveles[i] = niveles[i - 1] + 1
            else:
                niveles[i] = niveles[i - 1]
        return max(niveles) + 1 if niveles else 1

    def obtener_resumen(self):
        resumen = "ANÁLISIS DE TIEMPO DE EJECUCIÓN (T(n))\n"
        resumen += "="*50 + "\n"
        resumen += f"Función de tiempo estimada: {self.funcion_tiempo}\n"
        resumen += f"Complejidad asintótica: {self.complejidad}\n\n"
        resumen += "Desglose por líneas:\n"
        resumen += "\n".join(self.lineas_analizadas)

        resumen += "\n\nEXPLICACIÓN:\n"
        if "O(1)" in self.complejidad:
            resumen += "Complejidad constante - El tiempo no depende del tamaño de entrada."
        elif "O(log n)" in self.complejidad:
            resumen += "Complejidad logarítmica - Típico de algoritmos que dividen el problema en cada iteración."
        elif "O(n)" in self.complejidad:
            resumen += "Complejidad lineal - El tiempo crece proporcionalmente con el tamaño de entrada."
        elif "O(n²)" in self.complejidad:
            resumen += "Complejidad cuadrática - Típico de dos bucles anidados."
        elif "O(n^" in self.complejidad:
            grado = self.complejidad.split("^")[1].replace(")", "")
            resumen += f"Complejidad polinomial (grado {grado}) - Típico de {grado} bucles anidados."

        return resumen
