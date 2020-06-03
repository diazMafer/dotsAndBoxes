import numpy as np
from math import inf as infinity
import random

def getPossibleMoves(board):
    moves = []
    lines = 0
    for i in board:
        square = 0
        for j in i:
            if j == 99:
                moves.append([lines,square])
            square += 1
        lines += 1

    return moves

"""
    Algoritmo basado en codigo explicado en https://www.youtube.com/watch?v=l-hh51ncgDI
"""

def minimax(board, move, depth, maximazingPlayer, myId, alpha, beta):
    idPlayerPlaying = myId if maximazingPlayer else (myId % 2) + 1
    children = getPossibleMoves(board)
    actualScore = close_box(board, move, idPlayerPlaying, not maximazingPlayer)

    if depth == 0 or 99 not in np.asarray(board).reshape(-1) or actualScore != 0:
        return  [move, close_box(board, move, idPlayerPlaying, not maximazingPlayer)]

    if maximazingPlayer:
        best_move = []
        best_score = -infinity
        for movimiento in children:
            value = minimax(board, movimiento, depth - 1, False, idPlayerPlaying, alpha, beta)
            best_score = max(best_score, value[1])
            best_move.append(movimiento) 
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return [movimiento, best_score]

    else:
        worst_score = infinity
        worst_move = []
        for movimiento in children:
            value = minimax(board, movimiento, depth - 1, True, idPlayerPlaying, alpha, beta)
            worst_score = min(worst_score, value[1])
            worst_move.append(movimiento)
            beta = min(beta, worst_score)
            if beta <= alpha:
                break

        return [worst_move, worst_score]

def ai(board, playerId, depth):
    move = []
    score = -infinity
    children = getPossibleMoves(board)
    for movimiento in children:
        bestMove = minimax(board, movimiento, int(depth), True, int(playerId), -infinity, infinity)
        if bestMove[1] > score:
            score = bestMove[1]

        if bestMove[1] >= score:
            move = bestMove[0]
        
    finalMove = random.choice(move)
    if (type(finalMove) != int):
        return finalMove
    else: 
        return move

"""
    Método tomado de foro en canvas
    autor: David Uriel Soto
"""
def close_box(oldBoard, move, playerNumber, maximazingPlayer):
    N = 6
    EMPTY = 99
    board = oldBoard

    acumulador = 0
    contador = 0
    contadorPuntos = 0
    
    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                contadorPuntos = contadorPuntos + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0

    player1 = 0
    player2 = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2

    for i in range(len(board[0])):
        if board[0][i] == FILLEDP12:
            player1 = player1 + 2
        elif board[0][i] == FILLEDP11:
            player1 = player1 + 1
        elif board[0][i] == FILLEDP22:
            player2 = player2 + 2
        elif board[0][i] == FILLEDP21:
            player2 = player2 + 1

    for j in range(len(board[1])):
        if board[1][j] == FILLEDP12:
            player1 = player1 + 2
        elif board[1][j] == FILLEDP11:
            player1 = player1 + 1
        elif board[1][j] == FILLEDP22:
            player2 = player2 + 2
        elif board[1][j] == FILLEDP21:
            player2 = player2 + 1

    return player1 - player2 if maximazingPlayer else (-2) * (player1 - player2)


