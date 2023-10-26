import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Movimentos possíveis do cavalo
movimentos = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

tamanho_tabuleiro = 8

# Função para verificar se uma posição é válida no tabuleiro
def posicao_valida(x, y, tabuleiro):
    return 0 <= x < tamanho_tabuleiro and 0 <= y < tamanho_tabuleiro and tabuleiro[x][y] == 0

# Função para resolver o problema do cavalo usando busca em profundidade
def resolver_cavalo():
    tabuleiro = [[0 for _ in range(tamanho_tabuleiro)] for _ in range(tamanho_tabuleiro)]
    x, y = 0, 0  # Posição inicial
    tabuleiro[x][y] = 1
    movimento = 2
    caminho = [(x, y)]

    def dfs(x, y, movimento):
        if movimento == tamanho_tabuleiro ** 2:  # O cavalo visitou todas as casas
            return True

        for dx, dy in movimentos:
            novo_x, novo_y = x + dx, y + dy
            if posicao_valida(novo_x, novo_y, tabuleiro):
                tabuleiro[novo_x][novo_y] = movimento
                caminho.append((novo_x, novo_y))
                if dfs(novo_x, novo_y, movimento + 1):
                    return True
                tabuleiro[novo_x][novo_y] = 0
                caminho.pop()

        return False

    if dfs(x, y, movimento):
        print("Solução encontrada:")
        for linha in tabuleiro:
            print(linha)
        return caminho

    return None

caminho = resolver_cavalo()

print("Caminho do cavalo:")
print(caminho)


# Função para criar uma animação do movimento do cavalo com tabuleiro colorido e números
def animacao_movimento_cavalo(caminho):
    fig, ax = plt.subplots()
    ax.set_xlim(0, tamanho_tabuleiro)
    ax.set_ylim(0, tamanho_tabuleiro)
    
    tabuleiro = [[0 for _ in range(tamanho_tabuleiro)] for _ in range(tamanho_tabuleiro)]

    def init():
        return []

    def animate(i):
        x, y = caminho[i]
        tabuleiro[x][y] = i + 1  # Coloque o número correspondente ao quadrado
        ax.clear()
        ax.set_xlim(0, tamanho_tabuleiro)
        ax.set_ylim(0, tamanho_tabuleiro)

        for linha in range(tamanho_tabuleiro):
            for coluna in range(tamanho_tabuleiro):
                if tabuleiro[linha][coluna] > 0:
                    cor = 'black'
                    ax.text(coluna + 0.5, linha + 0.5, str(tabuleiro[linha][coluna]), ha='center', va='center', fontsize=10, color='white')
                elif (linha + coluna) % 2 == 0:
                    cor = 'white'
                else:
                    cor = 'green'
                ax.add_patch(plt.Rectangle((coluna, linha), 1, 1, color=cor))

        ax.plot(y + 0.5, x + 0.5, 'ro', markersize=15)  # Posicione o ponto no centro da casa

    ani = animation.FuncAnimation(fig, animate, frames=len(caminho), init_func=init, repeat=False, interval=200)  # Diminui a velocidade
    plt.show()

if caminho:
    print("Caminho encontrado!")
    animacao_movimento_cavalo(caminho)
else:
    print("Não foi encontrada uma solução para o problema do cavalo.")
