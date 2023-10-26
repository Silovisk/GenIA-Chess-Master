import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Tabuleiro:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.movimentos = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        self.tabuleiro = [[0 for _ in range(tamanho)] for _ in range(tamanho)]

    def posicao_valida(self, x, y):
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho and self.tabuleiro[x][y] == 0

    def marcar_posicao(self, x, y, valor):
        self.tabuleiro[x][y] = valor

    def limpar_posicao(self, x, y):
        self.tabuleiro[x][y] = 0

    def __str__(self):
        return '\n'.join([' '.join(map(str, linha)) for linha in self.tabuleiro])

class AlgoritmoGenetico:
    def __init__(self, tabuleiro, geracoes, tamanho_populacao):
        self.tabuleiro = tabuleiro
        self.geracoes = geracoes
        self.tamanho_populacao = tamanho_populacao

    def fitness(self, caminho):
        aptidao = 0
        tamanho_tabuleiro = self.tabuleiro.tamanho
        tabuleiro = Tabuleiro(tamanho_tabuleiro)

        for i, pos in enumerate(caminho):
            x, y = pos // tamanho_tabuleiro, pos % tamanho_tabuleiro
            tabuleiro.marcar_posicao(x, y, i + 1)

        for i, pos in enumerate(caminho):
            x, y = pos // tamanho_tabuleiro, pos % tamanho_tabuleiro
            for dx, dy in self.tabuleiro.movimentos:
                novo_x, novo_y = x + dx, y + dy
                if tabuleiro.posicao_valida(novo_x, novo_y):
                    aptidao += 1

        return len(set(caminho))  # Use the number of unique positions as fitness


    def crossover(self, pai1, pai2):
        ponto_de_corte = random.randint(1, len(pai1) - 1)
        filho = pai1[:ponto_de_corte] + [gene for gene in pai2 if gene not in pai1[:ponto_de_corte]]
        return filho

    def mutacao(self, individuo):
        indice1, indice2 = random.sample(range(len(individuo)), 2)
        individuo[indice1], individuo[indice2] = individuo[indice2], individuo[indice1]
        return individuo




    def encontrar_caminhos(self, limite=10):
        caminhos = []
        populacao_inicial = [random.sample(range(self.tabuleiro.tamanho ** 2), self.tabuleiro.tamanho ** 2) for _ in range(self.tamanho_populacao)]
        populacao = populacao_inicial

        for geracao in range(self.geracoes):
            populacao = sorted(populacao, key=lambda x: self.fitness(x), reverse=True)
            melhor_individuo = populacao[0]
            print(f"Geração {geracao + 1}: Aptidão do melhor indivíduo = {self.fitness(melhor_individuo)}")

            for individuo in populacao:
                if self.fitness(individuo) == self.tabuleiro.tamanho ** 2:
                    caminho = [(i // self.tabuleiro.tamanho, i % self.tabuleiro.tamanho) for i in individuo]
                    caminhos.append(caminho)

                if len(caminhos) >= limite:
                    return caminhos

            nova_populacao = [melhor_individuo]

            while len(nova_populacao) < len(populacao):
                pai1, pai2 = random.choices(populacao[:10], k=2)
                filho = self.crossover(pai1, pai2)
                if random.random() < 0.1:
                    filho = self.mutacao(filho)
                nova_populacao.append(filho)

            populacao = nova_populacao

        return caminhos


class AnimacaoMovimentoCavalo:
    def __init__(self, caminho, tamanho_tabuleiro):
        self.caminho = caminho
        self.tamanho_tabuleiro = tamanho_tabuleiro

    def criar_animacao(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.tamanho_tabuleiro)
        ax.set_ylim(0, self.tamanho_tabuleiro)
        tabuleiro = Tabuleiro(self.tamanho_tabuleiro)

        def init():
            return []

        def animate(i):
            x, y = self.caminho[i]
            tabuleiro.marcar_posicao(x, y, i + 1)
            ax.clear()
            ax.set_xlim(0, self.tamanho_tabuleiro)
            ax.set_ylim(0, self.tamanho_tabuleiro)

            for linha in range(self.tamanho_tabuleiro):
                for coluna in range(self.tamanho_tabuleiro):
                    if tabuleiro.tabuleiro[linha][coluna] > 0:
                        cor = 'black'
                        ax.text(coluna + 0.5, linha + 0.5, str(tabuleiro.tabuleiro[linha][coluna]), ha='center', va='center', fontsize=10, color='white')
                    elif (linha + coluna) % 2 == 0:
                        cor = 'white'
                    else:
                        cor = 'green'
                    ax.add_patch(plt.Rectangle((coluna, linha), 1, 1, color=cor))

            ax.plot(y + 0.5, x + 0.5, 'ro', markersize=15)

        ani = animation.FuncAnimation(fig, animate, frames=len(self.caminho), init_func=init, repeat=False, interval=200)
        plt.show()

def main():
    tamanho_tabuleiro = 8
    tabuleiro = Tabuleiro(tamanho_tabuleiro)
    algoritmo_genetico = AlgoritmoGenetico(tabuleiro, geracoes=300, tamanho_populacao=150)
    caminhos = algoritmo_genetico.encontrar_caminhos(limite=10)
    
    print(f"Encontrados {len(caminhos)} caminhos onde o cavalo ataca a casa em que iniciou o movimento:")

    for i, caminho in enumerate(caminhos):
        print(f"Caminho {i + 1}:")
        print('\n'.join([' '.join(map(str, linha)) for linha in tabuleiro.tabuleiro]))
        print()

        animacao = AnimacaoMovimentoCavalo(caminho, tamanho_tabuleiro)
        animacao.criar_animacao()

if __name__ == "__main__":
    main()
