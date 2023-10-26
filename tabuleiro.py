import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

chess_notation_queens = [
    "A1",
    "B2",
    "C3",
    "D4",
    "E5",
    "F6",
    "G7",
    "H8",
    "I9",
    "J10",
    "K11",
    "L12",
]

letras = []
numeros = []

# Pegar todos os valores de chess_notation_queens e colocar em um array
for chess_notation_queen in chess_notation_queens:
    letras.append(chess_notation_queen[0])
    numeros.append(int(chess_notation_queen[1]))  # Converte para inteiro

print(letras)
print(numeros)

chess_top = sorted(letras)
chess_left = sorted(numeros)
tamanho_tabuleiro = max(max(numeros)) + 1  # Adicione 1 para acomodar o tamanho máximo

tabuleiro = np.tile([1, 0], (tamanho_tabuleiro, tamanho_tabuleiro))[:tamanho_tabuleiro, :tamanho_tabuleiro]

for i in range(tabuleiro.shape[0]):
    tabuleiro[i] = np.roll(tabuleiro[i], i % 2)

tabuleiro = np.flipud(tabuleiro)  # Transpõe o tabuleiro

mapa_de_cores = ListedColormap(["white", "black"])
plt.matshow(tabuleiro, cmap=mapa_de_cores)

# adicione as notaçoes de xadrez na parte baixo que é chess_bottom
plt.xticks(range(tamanho_tabuleiro), chess_top[:tamanho_tabuleiro])
plt.yticks(range(tamanho_tabuleiro), chess_left[:tamanho_tabuleiro])
plt.show()
