import math

class FuncionTiempo:
    """
    Representa una función de tiempo y maneja las operaciones relacionadas
    """
    
    def __init__(self, expresion="", notacion="O(1)"):
        self.expresion = expresion
        self.notacion_asintotica = notacion
        self.valores_calculados = {}
        
    def generar_funcion(self, complejidad):
        """
        Genera la función matemática basada en la complejidad
        """
        if complejidad == "O(1)":
            self.expresion = "1"
            self.notacion_asintotica = "O(1)"
        elif complejidad == "O(n)":
            self.expresion = "n"
            self.notacion_asintotica = "O(n)"
        elif complejidad == "O(n²)":
            self.expresion = "n²"
            self.notacion_asintotica = "O(n²)"
        elif complejidad == "O(n³)":
            self.expresion = "n³"
            self.notacion_asintotica = "O(n³)"
        elif "log" in complejidad:
            self.expresion = "n*log(n)"
            self.notacion_asintotica = "O(n log n)"
        else:
            self.expresion = complejidad.replace("O(", "").replace(")", "")
            self.notacion_asintotica = complejidad
    
    def calcular_valores(self, rango_n):
        """
        Calcula los valores de la función para un rango dado
        """
        valores = []
        for n in rango_n:
            if n <= 0:
                valores.append(0)
                continue
                
            if self.notacion_asintotica == "O(1)":
                valores.append(1)
            elif self.notacion_asintotica == "O(n)":
                valores.append(n)
            elif self.notacion_asintotica == "O(n²)":
                valores.append(n * n)
            elif self.notacion_asintotica == "O(n³)":
                valores.append(n * n * n)
            elif self.notacion_asintotica == "O(n log n)":
                valores.append(n * math.log2(n) if n > 0 else 0)
            elif self.notacion_asintotica == "O(log n)":
                valores.append(math.log2(n) if n > 0 else 0)
            else:
                valores.append(n)  # Default
                
        return valores
    
    def comparar(self, otra_funcion):
        """
        Compara esta función con otra
        """
        orden_complejidad = {
            "O(1)": 1,
            "O(log n)": 2,
            "O(n)": 3,
            "O(n log n)": 4,
            "O(n²)": 5,
            "O(n³)": 6
        }
        
        valor_actual = orden_complejidad.get(self.notacion_asintotica, 10)
        valor_otra = orden_complejidad.get(otra_funcion.notacion_asintotica, 10)
        
        if valor_actual < valor_otra:
            return "Más eficiente"
        elif valor_actual == valor_otra:
            return "Igual eficiencia"
        else:
            return "Menos eficiente"