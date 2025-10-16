from src.utils.prints import printMRH, printAlumno
from src.enviroment import Environment
from src.utils.temporal_data import alumno, MRH, ALL_REACTIVOS

env = Environment(population_size=50, all_reactivos=ALL_REACTIVOS)
best_individuals = env.run_evolution(student_profile=alumno, MRH=MRH, generations=10, top_n=3)

for i, ind in enumerate(best_individuals, 1):
    print(f"Top {i}: {ind}")

printMRH()
printAlumno()
