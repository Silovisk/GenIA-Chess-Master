import numpy as np

def solve(bo, row, col, n, counter):
    if counter == n * n:
        return True

    for i in range(8):
        new_x = row + move_x[i]
        new_y = col + move_y[i]
        if validateMove(bo, new_x, new_y, n):
            bo[new_x, new_y] = counter
            if solve(bo, new_x, new_y, n, counter + 1):
                return True
            bo[new_x, new_y] = 0
    return False

def validateMove(bo, row, col, n):
    return 0 <= row < n and 0 <= col < n and bo[row, col] == 0

def knights_tour(board_size, start_row, start_col):
    n = board_size
    board = np.zeros((n, n))
    board[start_row, start_col] = 1
    global move_x, move_y
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]
    
    if solve(board, start_row, start_col, n, 2):
        print("Solution found:")
        print(board)
        print("Total moves:", board.sum())
    else:
        print("No solution found.")

board_size = 8  # Tamanho do tabuleiro
start_row = 3    # Posição inicial da linha
start_col = 2    # Posição inicial da coluna
knights_tour(board_size, start_row, start_col)
