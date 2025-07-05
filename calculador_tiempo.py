import re
import math
from tkinter import messagebox

class CalculadorTiempo:
    """
    Calcula el tiempo de ejecución T(n) de un algoritmo en Python
    basado en el conteo de Operaciones Elementales (OE) y análisis de bucles
    """
    
    def __init__(self):
        self.contador_oe = 0
        self.lineas_analizadas = []
        self.funcion_tiempo = ""
        self.complejidad = "O(1)"
        
    def analizar_codigo(self, codigo):
        """Analiza el código y calcula el tiempo T(n) en función de n"""
        self.contador_oe = 0
        self.lineas_analizadas = []
        self.funcion_tiempo = ""
        self.complejidad = "O(1)"
        
        try:
            # Primero analizamos las líneas para contar OE
            lineas = codigo.split('\n')
            for linea in lineas:
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue
                    
                self._analizar_linea(linea)
            
            # Luego analizamos la estructura para determinar T(n)
            self._determinar_funcion_tiempo(codigo)
            
            return self.contador_oe
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el código: {str(e)}")
            return 0
    
    def _analizar_linea(self, linea):
        """Analiza una línea de código individual"""
        oe_linea = 0
        
        # Asignaciones
        if ':=' in linea or '=' in linea.split()[0]:
            oe_linea += self._contar_declaracion(linea)
        
        # Condicionales
        elif linea.startswith(('if ', 'elif ')):
            oe_linea += self._contar_condicional(linea)
        
        # Bucles
        elif linea.startswith(('for ', 'while ')):
            oe_linea += self._contar_bucle(linea)
        
        # Llamadas a funciones
        elif '(' in linea and ')' in linea:
            oe_linea += self._contar_llamada_funcion(linea)
        
        # Operaciones aritméticas/lógicas
        else:
            oe_linea += self._contar_operaciones(linea)
        
        self.contador_oe += oe_linea
        self.lineas_analizadas.append(f"{linea} // OE: {oe_linea}")
    
    def _contar_declaracion(self, linea):
        """Cuenta OE en declaraciones de variables"""
        if '=' in linea:
            partes = linea.split('=')
            # 1 OE por la asignación + operaciones en el valor
            return 1 + self._contar_operaciones(partes[1])
        return 0
    
    def _contar_condicional(self, linea):
        """Cuenta OE en condicionales"""
        # 1 OE por evaluar la condición + operaciones en la condición
        condicion = linea[linea.find('(')+1:linea.rfind(')')]
        return 1 + self._contar_operaciones(condicion)
    
    def _contar_bucle(self, linea):
        """Cuenta OE en bucles for/while"""
        if linea.startswith('for'):
            return self._contar_for(linea)
        else:  # while
            return self._contar_while(linea)
    
    def _contar_for(self, linea):
        """Cuenta OE en un bucle for"""
        # 1 OE por la iteración + operaciones en el rango
        if ' in ' in linea:
            condition = linea.split(' in ')[1].strip()
            return 1 + self._contar_operaciones(condition)
        return 0
    
    def _contar_while(self, linea):
        """Cuenta OE en un bucle while"""
        # 1 OE por evaluar la condición + operaciones en la condición
        condicion = linea[linea.find('(')+1:linea.rfind(')')]
        return 1 + self._contar_operaciones(condicion)
    
    def _contar_llamada_funcion(self, linea):
        """Cuenta OE en llamadas a funciones"""
        # 1 OE por la llamada + operaciones en los parámetros
        parametros = linea[linea.find('(')+1:linea.rfind(')')]
        return 1 + (self._contar_operaciones(parametros) if parametros else 0)
    
    def _contar_operaciones(self, expresion):
        """Cuenta OE en una expresión aritmética/lógica"""
        if not expresion.strip():
            return 0
            
        # Contar operadores básicos
        operadores = r'\+|\-|\*|\/|\%|\*\*|\/\/|==|!=|<=|>=|<|>|and|or|not'
        matches = re.findall(operadores, expresion)
        oe = len(matches)
        
        # Contar asignaciones compuestas
        if any(op in expresion for op in ['+=', '-=', '*=', '/=']):
            oe += 1
        
        return oe
    
    def _determinar_funcion_tiempo(self, codigo):
        """
        Determina la función de tiempo T(n) basada en la estructura del código
        y el conteo de OE, especialmente para bucles
        """
        # Analizar bucles for
        for_lines = [line for line in codigo.split('\n') if line.strip().startswith('for')]
        while_lines = [line for line in codigo.split('\n') if line.strip().startswith('while')]
        
        # Si hay bucles for, determinamos T(n)
        if for_lines:
            self._analizar_bucles_for(for_lines)
        elif while_lines:
            self._analizar_bucles_while(while_lines)
        else:
            # Sin bucles, complejidad constante
            self.funcion_tiempo = f"T(n) = {self.contador_oe}"
            self.complejidad = "O(1)"
    
    def _analizar_bucles_for(self, for_lines):
        """
        Analiza bucles for para determinar T(n) como en el ejemplo proporcionado
        """
        # Contamos el número de bucles for anidados
        num_bucles = len(for_lines)
        
        if num_bucles == 1:
            # Bucle simple - complejidad lineal O(n)
            oe_cuerpo = self._estimar_oe_cuerpo_bucle(for_lines[0])
            oe_inicializacion = 1
            oe_comparacion = 1
            oe_incremento = 2
            
            t_bucle = oe_inicializacion + oe_comparacion
            t_bucle += f" + n * ({oe_cuerpo} + {oe_comparacion} + {oe_incremento})"
            
            # Sumamos las OE fuera del bucle
            oe_fuera = self.contador_oe - (oe_inicializacion + oe_comparacion)
            
            self.funcion_tiempo = f"T(n) = {oe_fuera} + {t_bucle}"
            self.complejidad = "O(n)"
            
        elif num_bucles == 2:
            # Dos bucles anidados - complejidad cuadrática O(n²)
            self.funcion_tiempo = "T(n) = a + b*n + c*n²"
            self.complejidad = "O(n²)"
        else:
            # Más de dos bucles anidados
            self.funcion_tiempo = f"T(n) = polinomio de grado {num_bucles}"
            self.complejidad = f"O(n^{num_bucles})"
    
    def _analizar_bucles_while(self, while_lines):
        """
        Analiza bucles while para determinar T(n) como en el ejemplo logarítmico
        """
        # Buscamos patrones de división (como en el ejemplo logarítmico)
        div_pattern = r'\w+\s*<-\s*\w+\s*div\s*\d+'
        for line in while_lines:
            if re.search(div_pattern, line, re.IGNORECASE):
                # Patrón logarítmico encontrado
                self.funcion_tiempo = "T(n) = a*log(n) + b"
                self.complejidad = "O(log n)"
                return
        
        # Si no encontramos patrones especiales, asumimos lineal
        self.funcion_tiempo = "T(n) = a*n + b"
        self.complejidad = "O(n)"
    
    def _estimar_oe_cuerpo_bucle(self, linea_for):
        """
        Estima las OE dentro del cuerpo de un bucle for
        (implementación simplificada)
        """
        # En una implementación real, analizaríamos el cuerpo del bucle
        return 3  # Valor por defecto basado en el ejemplo
    
    def obtener_resumen(self):
        """Genera un resumen detallado del análisis"""
        resumen = "ANÁLISIS DE TIEMPO DE EJECUCIÓN (T(n))\n"
        resumen += "="*50 + "\n"
        resumen += f"Total de Operaciones Elementales (OE): {self.contador_oe}\n"
        resumen += f"Función de tiempo estimada: {self.funcion_tiempo}\n"
        resumen += f"Complejidad asintótica: {self.complejidad}\n\n"
        resumen += "Desglose por líneas:\n"
        resumen += "\n".join(self.lineas_analizadas)
        
        # Añadir explicación según el tipo de complejidad
        resumen += "\n\nEXPLICACIÓN:\n"
        if "O(1)" in self.complejidad:
            resumen += "Complejidad constante - El tiempo no depende del tamaño de entrada."
        elif "O(log n)" in self.complejidad:
            resumen += ("Complejidad logarítmica - Típico de algoritmos que dividen "
                      "el problema en cada iteración (ej. búsqueda binaria).")
        elif "O(n)" in self.complejidad:
            resumen += ("Complejidad lineal - El tiempo crece proporcionalmente con "
                      "el tamaño de entrada (ej. un bucle simple).")
        elif "O(n²)" in self.complejidad:
            resumen += ("Complejidad cuadrática - Típico de dos bucles anidados. "
                      "El tiempo crece con el cuadrado del tamaño de entrada.")
        elif "O(n^" in self.complejidad:
            grado = self.complejidad.split("^")[1].replace(")", "")
            resumen += (f"Complejidad polinomial (grado {grado}) - Típico de "
                       f"{grado} bucles anidados. El tiempo crece rápidamente con el tamaño de entrada.")
        
        return resumen