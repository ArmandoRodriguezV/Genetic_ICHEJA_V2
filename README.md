# Documentación del Modelo de Algoritmo Genético (AG) para la Selección de Reactivos

## 1. Introducción

Este proyecto implementa un **Algoritmo Genético (AG)** diseñado para optimizar la selección de un conjunto de reactivos (ítems de evaluación) que mejor se adapten al perfil de habilidades de un estudiante. El objetivo principal es identificar los reactivos que, al ser aplicados, maximicen la evaluación de las habilidades que el estudiante necesita reforzar (aquellas con un nivel de dominio bajo), al mismo tiempo que se consideran las habilidades de alto dominio y se penaliza la redundancia.

El modelo opera bajo el principio de la evolución natural, donde los "individuos" (conjuntos de reactivos) compiten, se cruzan y mutan a lo largo de varias generaciones para encontrar la solución óptima.

## 2. Estructura del Proyecto

El código fuente está organizado en los siguientes archivos principales:

```
nuevo_Ag/
├── app.py
└── src/
    ├── enviroment.py
    ├── individual.py
    └── utils/
        ├── prints.py
        └── temporal_data.py
```

| Archivo | Descripción |
| :--- | :--- |
| `app.py` | Punto de entrada de la aplicación. Inicializa el entorno, ejecuta el proceso evolutivo y muestra los resultados. |
| `src/enviroment.py` | Contiene la clase `Environment`, que gestiona la población, la selección de padres, el cruce, la mutación y el ciclo de evolución. |
| `src/individual.py` | Define la clase `Individual`, que representa un conjunto de reactivos y contiene la lógica para calcular la función de aptitud (fitness). |
| `src/utils/temporal_data.py` | Almacena los datos de configuración iniciales: la lista de reactivos, el mapeo de reactivos a habilidades (`MRH`) y el perfil de dominio del estudiante (`alumno`). |
| `src/utils/prints.py` | Funciones auxiliares para la presentación de los datos iniciales (`MRH` y `alumno`) en formato tabular. |

## 3. Componentes del Algoritmo Genético

### 3.1. El Individuo (`Individual`)

Un individuo en este modelo representa un **conjunto de exactamente 3 reactivos** seleccionados de la lista total disponible.

*   **Genotipo**: La lista de 3 reactivos (ej. `["R1", "R5", "R12"]`).
*   **Fenotipo**: El valor de aptitud (`fitness`) calculado para ese conjunto de reactivos.

### 3.2. Función de Aptitud (Fitness)

La función de aptitud es el corazón del algoritmo, ya que determina qué tan "bueno" es un conjunto de reactivos para el estudiante. El cálculo se basa en tres criterios principales, cada uno con un peso específico:

$$
\text{Fitness} = \alpha \cdot \text{Puntuación\_No\_Aprobada} + \beta \cdot \text{Bono\_Puntuación\_Alta} + \gamma \cdot \text{Penalización\_Repetición}
$$

| Componente | Descripción | Peso (Variable) | Valor |
| :--- | :--- | :--- | :--- |
| **Puntuación No Aprobada** | Suma de las diferencias $(1 - \text{Nivel})$ para cada habilidad cubierta por los reactivos cuyo nivel de dominio es **menor a 0.7**. **Objetivo**: Maximizar la cobertura de habilidades que necesitan refuerzo. | $\alpha$ | 0.6 |
| **Bono Puntuación Alta** | Suma de los niveles de dominio para cada habilidad cubierta cuyo nivel es **mayor o igual a 0.7**. Se aplica un factor de 0.3 a esta suma. **Objetivo**: Considerar las habilidades de alto dominio con un peso menor. | $\beta$ | 0.3 |
| **Penalización Repetición** | Se calcula como $\frac{\text{Reactivos\_Únicos}}{3}$. El valor es 1 si los 3 reactivos son distintos, y menor si hay repeticiones. **Objetivo**: Minimizar la selección de reactivos duplicados. | $\gamma$ | 0.1 |

### 3.3. El Entorno (`Environment`)

La clase `Environment` orquesta el proceso evolutivo:

1.  **Población Inicial**: Se crea una población de 50 individuos, donde cada individuo es un conjunto aleatorio de 3 reactivos.
2.  **Selección de Padres**: Se utiliza el método de **Selección por Torneo** con un tamaño de torneo de 3. Los dos individuos con el *fitness* más alto dentro del torneo son seleccionados como padres.
3.  **Cruce (Crossover)**: Se implementa un cruce basado en la unión de los reactivos de ambos padres. Los reactivos del hijo son la unión de los reactivos del Padre 1 y el Padre 2. Si el número total de reactivos únicos es mayor a 3, se seleccionan 3 reactivos de forma aleatoria de ese conjunto.
4.  **Mutación**: Se aplica una tasa de mutación del **30%** (`mutation_rate=0.3`). Si ocurre la mutación, uno de los 3 reactivos del individuo es reemplazado por un reactivo seleccionado al azar de la lista total que no esté ya en el individuo.
5.  **Evolución**: El proceso se repite por un número definido de generaciones (10 en la configuración de `app.py`). En cada generación, se crea una nueva población a partir de la selección, cruce y mutación de los individuos de la generación anterior.

## 4. Configuración y Ejecución

### 4.1. Datos Iniciales (`temporal_data.py`)

El modelo utiliza los siguientes datos de ejemplo:

*   **`ALL_REACTIVOS`**: 20 reactivos, de "R1" a "R20".
*   **`MRH` (Mapeo Reactivo-Habilidad)**: Un diccionario que asocia cada reactivo con las habilidades que evalúa. Por ejemplo, `"R1": ["H1", "H3", "H5"]`.
*   **`alumno` (Perfil del Estudiante)**: Un diccionario que indica el nivel de dominio (entre 0.0 y 1.0) del estudiante en 10 habilidades ("H1" a "H10").

| Habilidad | Nivel de Dominio | Estado (Nivel < 0.7) |
| :--- | :--- | :--- |
| H1 | 0.71 | Aprobado |
| H2 | 0.78 | Aprobado |
| H3 | 0.95 | **Reprobado** |
| H4 | 0.98 | Aprobado |
| H5 | 0.85 | Aprobado |
| H6 | 0.97 | **Reprobado** |
| H7 | 0.91 | Aprobado |
| H8 | 0.23 | **Reprobado** |
| H9 | 0.95 | **Reprobado** |
| H10 | 0.62 | **Reprobado** |

*Nota: El estado "Reprobado" en el perfil del estudiante indica un nivel de dominio bajo (menor a 0.7) que el algoritmo genético intentará maximizar su cobertura.*

### 4.2. Ejecución

El proceso de ejecución se define en `app.py`:

1.  Se inicializa el entorno: `env = Environment(population_size=50, all_reactivos=ALL_REACTIVOS)`.
2.  Se ejecuta la evolución: `best_individuals = env.run_evolution(student_profile=alumno, MRH=MRH, generations=10, top_n=3)`.
3.  El resultado son los **3 mejores individuos** (conjuntos de reactivos) encontrados después de 10 generaciones, ordenados por su valor de aptitud (`fitness`).

## 5. Requisitos y Dependencias

El proyecto requiere la librería `tabulate` para la presentación tabular de los datos iniciales.

```bash
pip install tabulate
```

## 6. Uso

Para ejecutar el modelo y obtener los reactivos óptimos, simplemente ejecute el archivo principal:

```bash
python app.py
```

El programa imprimirá en la consola los 3 conjuntos de reactivos con el mayor *fitness* y, posteriormente, las tablas de mapeo Reactivo-Habilidad y el perfil del estudiante.

