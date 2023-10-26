import random

class NQueens:
    def __init__(self, N):
        self.N = N
        self.board = [-1] * N  # Inicialize com -1, indicando que não há rainhas em nenhuma coluna.
        self.fitness = 0

    def calculate_fitness(self):
        self.fitness = 0
        for i in range(self.N):
            for j in range(i+1, self.N):
                if self.board[i] == self.board[j] or abs(i - j) == abs(self.board[i] - self.board[j]):
                    self.fitness += 1

    def randomize_board(self):
        self.board = [random.randint(0, self.N - 1) for _ in range(self.N)]

    def crossover(self, other):
        midpoint = random.randint(1, self.N - 1)
        child = NQueens(self.N)
        child.board[:midpoint] = self.board[:midpoint]
        for gene in other.board:
            if gene not in child.board:
                for i in range(self.N):
                    if child.board[i] == -1:
                        child.board[i] = gene
                        break
        return child

    def mutate(self):
        index = random.randint(0, self.N - 1)
        new_position = random.randint(0, self.N - 1)
        while new_position == self.board[index]:
            new_position = random.randint(0, self.N - 1)
        self.board[index] = new_position

def genetic_algorithm(N, population_size, max_generations):
    population = [NQueens(N) for _ in range(population_size)]
    
    def convert_to_chess_notation(board):
        chess_notation = []
        for i in range(len(board)):
            row = board[i]
            column_letter = chr(ord('A') + row)
            chess_notation.append(f"{column_letter}{i + 1}")
        return chess_notation
    
    for generation in range(max_generations):
        for individual in population:
            individual.randomize_board()
            individual.calculate_fitness()
        
        population.sort(key=lambda x: x.fitness)
        if population[0].fitness == 0:
            print("Solução encontrada na geração", generation)
            print("Tabuleiro da solução:")
            chess_notation = convert_to_chess_notation(population[0].board)
            for position in chess_notation:
                print(position)
            break
        
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.sample(population[:population_size // 2], 2)
            child1 = parent1.crossover(parent2)
            child2 = parent2.crossover(parent1)
            child1.mutate()
            child2.mutate()
            new_population.extend([child1, child2])
        
        population = new_population

    if population[0].fitness > 0:
        print("Nenhuma solução encontrada após", max_generations, "gerações.")

if __name__ == "__main__":
    N = 8
    population_size = 100
    max_generations = 1000
    genetic_algorithm(N, population_size, max_generations)
