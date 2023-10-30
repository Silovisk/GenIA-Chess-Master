import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class AnimacaoMovimentoCavalo:
    def __init__(self, matrix):
        self.matrix = matrix
        self.tamanho_tabuleiro = matrix.shape[0]

    def criar_animacao(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.tamanho_tabuleiro)
        ax.set_ylim(0, self.tamanho_tabuleiro)
        chessboard = np.zeros((self.tamanho_tabuleiro, self.tamanho_tabuleiro), dtype=int)

        def init():
            return []

        def animate(i):
            posicao = i + 1
            x, y = np.where(self.matrix == posicao)
            x, y = x[0], y[0]
            chessboard[x, y] = posicao
            ax.clear()
            ax.set_xlim(0, self.tamanho_tabuleiro)
            ax.set_ylim(0, self.tamanho_tabuleiro)

            for linha in range(self.tamanho_tabuleiro):
                for coluna in range(self.tamanho_tabuleiro):
                    if chessboard[linha, coluna] > 0:
                        cor = 'black'
                        ax.text(coluna + 0.5, linha + 0.5, str(chessboard[linha, coluna]), ha='center', va='center', fontsize=10, color='white')
                    elif (linha + coluna) % 2 == 0:
                        cor = 'white'
                    else:
                        cor = 'green'
                    ax.add_patch(plt.Rectangle((coluna, linha), 1, 1, color=cor))

            ax.plot(y + 0.5, x + 0.5, 'ro', markersize=15)

        ani = animation.FuncAnimation(fig, animate, frames=self.tamanho_tabuleiro * self.tamanho_tabuleiro, init_func=init, repeat=False, interval=500)
        plt.show()

# Your matrix
matrix = np.array([[38, 53, 30, 57, 14, 63, 28, 7],
                  [31, 58, 39, 62, 29, 8, 13, 64],
                  [52, 37, 54, 25, 56, 15, 6, 27],
                  [59, 32, 1, 40, 61, 26, 9, 12],
                  [36, 51, 60, 55, 24, 11, 16, 5],
                  [45, 48, 33, 2, 41, 18, 21, 10],
                  [50, 35, 46, 43, 20, 23, 4, 17],
                  [47, 44, 49, 34, 3, 42, 19, 22]])

# Create an instance of AnimacaoMovimentoCavalo and start the animation
animacao = AnimacaoMovimentoCavalo(matrix)
animacao.criar_animacao()
