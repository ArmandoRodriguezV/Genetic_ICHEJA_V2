import random
from src.individual import Individual

class Environment:
    def __init__(self, population_size, all_reactivos):
        self.population_size = population_size
        self.all_reactivos = all_reactivos
        self.population = self._create_initial_population()

    def _create_initial_population(self):
        population = []
        for _ in range(self.population_size):
            reactivos = random.sample(self.all_reactivos, 3)
            population.append(Individual(reactivos))
        return population

    def select_parents(self):
        tournament_size = 3
        tournament = random.sample(self.population, tournament_size)
        tournament.sort(key=lambda x: x.fitness, reverse=True)
        return tournament[0], tournament[1]

    def crossover(self, parent1, parent2):
        child_reactivos = list(set(parent1.reactivos + parent2.reactivos))
        if len(child_reactivos) > 3:
            child_reactivos = random.sample(child_reactivos, 3)
        return Individual(child_reactivos)

    def mutate(self, individual, mutation_rate=0.3):
        if random.random() < mutation_rate:
            idx = random.randint(0, 2)
            new_reactivo = random.choice([r for r in self.all_reactivos if r not in individual.reactivos])
            individual.reactivos[idx] = new_reactivo
        return individual

    def next_generation(self):
        new_population = []
        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)
        self.population = new_population

    def run_evolution(self, student_profile, MRH, generations=10, top_n=3):
        for ind in self.population:
            ind.evaluate_fitness(student_profile, MRH)
            
        for _ in range(generations):
            self.next_generation()
            for ind in self.population:
                ind.evaluate_fitness(student_profile, MRH)

        top_individuals = sorted(self.population, key=lambda x: x.fitness, reverse=True)[:top_n]
        return top_individuals
