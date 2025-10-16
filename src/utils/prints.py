from tabulate import tabulate 
from src.utils.temporal_data import MRH, alumno

def printMRH():
    tabla = [[reactivo, ", ".join(habilidades)] for reactivo, habilidades in MRH.items()]
    print(tabulate(tabla, headers=["Reactivo", "Habilidades"], tablefmt="fancy_grid"))
    
def printAlumno():
    tabla = [[habilidad, nivel] for habilidad, nivel in alumno.items()]
    print(tabulate(tabla, headers=["Habilidad", "Nivel"], tablefmt="fancy_grid"))