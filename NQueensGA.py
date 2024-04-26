import random
import time

class GeneticNQueens:
    def __init__(self, N=64, population_size=100, mutation_rate=0.5, crossover_rate=0.8, generations=1000):
        self.N = N
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.population = []

    def initialize_population(self):
        for _ in range(self.population_size):   # Exemplo: N = 8
            individual = list(range(self.N))    # individual = [0,1,2,3,4,5,6,7]
            random.shuffle(individual)          # individual = [2,5,4,6,1,0,3,7]
            self.population.append(individual)  # adiciona indivíduo à população

    def fitness(self, individual):
        clashes = 0
        for i in range(len(individual)):
            for j in range(i + 1, len(individual)):
                if abs(i - j) == abs(individual[i] - individual[j]): # checa se há colisão
                    clashes += 1
        return clashes  # 0 colisões implica que o problema foi resolvido

    def selection(self):
        sorted_population = sorted(self.population, key=lambda x: self.fitness(x))  # ordena por fitness
        selected = sorted_population[:self.population_size // 2]    # selected é a metade da população com maior fitness
        return selected

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, self.N - 1)
        child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
        child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
        return child1, child2

    def mutate(self, individual):
        # if rand(0.0 ~ 1.0) < 0.5 (50% de chance da mutação ocorrer)
        if random.random() < self.mutation_rate: 
            idx1, idx2 = random.sample(range(self.N), 2) # dois numeros aleatorios e diferentes de 0 a 7
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
            #   mutação trocas duas posições aleatórias
    
    def fitness_average(self, population): # calcula a média de fitness de uma população
        average = 0
        for individual in population:
            average += self.fitness(individual)
        return average / len(population)

    def evolve(self):

        inicio_algoritmo = time.time()

        print("|\t---------------------------------------------------------------------------------------\t|")
        
        self.initialize_population()    # inicia população

        for i in range(self.generations): # 1000 gerações
            inicio = time.time()

            selected = self.selection() # seleciona a metade mais adaptada da populção
            new_population = []

            while len(new_population) < self.population_size: # while len(new_population) < 100

                parent1, parent2 = random.sample(selected, 2) # pega dois indivíduos aleatórios que foram selecionados

                if random.random() < self.crossover_rate: # if rand(0.0 ~ 1.0) < 0.8 (80% de chance do crossover ocorrer)
                    child1, child2 = self.crossover(parent1, parent2)

                    #   tentativa de mutação
                    self.mutate(child1)
                    self.mutate(child2)

                    new_population.append(child1)
                    new_population.append(child2)
                else:
                    new_population.append(parent1)
                    new_population.append(parent2)

            self.population = new_population    # atualiza a população com a nova geração
            
            best_individual = min(self.population, key=lambda x: self.fitness(x)) # pega indivíduo mais adaptado
            best_individual_fitness = self.fitness(best_individual)
            fitness_average = self.fitness_average(self.population)

            if (best_individual_fitness == 0):
                solution_found = "Sim"
            else:
                solution_found = "Não"

            fim = time.time()

            tempoProc = (fim - inicio) * 1000

            print(f"|\t Geração: {i + 1} | Solução Encontrada: {solution_found}")
            print(f"|\t Melhor Indivíduo: {best_individual}")
            print(f"|\t Melhor Fitness: {best_individual_fitness}")
            print(f"|\t Média de Fitness: {fitness_average:.4f} | Tempo de Processamento: {tempoProc:.4f} ms")
            print("|\t---------------------------------------------------------------------------------------\t|")
        
        fim_algoritmo = time.time()
        tempoProc_algoritmo = (fim_algoritmo - inicio_algoritmo) 
        print(f"\tTempo total de execução do algoritmo em {self.generations} gerações: {tempoProc_algoritmo:.4f} segundos")
        print(f"\tTamanho do tabuleiro: {self.N} x {self.N}")

        
        
if __name__ == "__main__":
    genetic_solver = GeneticNQueens()
    genetic_solver.evolve()
