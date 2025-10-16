class Individual:
    def __init__(self, reactivos):
        if len(reactivos) != 3:
            raise ValueError("Un individuo debe tener exactamente 3 reactivos")
        
        self.reactivos = reactivos
        self.fitness = 0.0

    def __repr__(self):
        return f"Individual({self.reactivos}, fitness={self.fitness:.3f})"

    def evaluate_fitness(self, student_profile, MRH):
        """
        Es casí el mismo criterio que dejo el doc. Carlos pero ahora con lo que pidio el profe Alí en la junta
        - Maximizar habilidades no aprobadas
        - Maximizar habilidades altas (peso menor)
        - Minimizar repeticiones
        """
        
        repetition_penalty = len(set(self.reactivos)) / 3  # 1 si todos distintos

        unpassed_score = 0
        high_score_bonus = 0
        for r in self.reactivos:
            for h in MRH[r]:
                score = student_profile[h]
                if score < 0.7:
                    unpassed_score += 1 - score   # más baja → mayor contribución
                else:
                    high_score_bonus += score * 0.3  # menor contribución

        # 3️⃣ Pesos
        alpha = 0.6
        beta = 0.3
        gamma = 0.1

        # 4️⃣ Fitness total
        self.fitness = alpha * unpassed_score + beta * high_score_bonus + gamma * repetition_penalty
