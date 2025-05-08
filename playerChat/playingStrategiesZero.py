import itertools
import math


def minimax_search(game, state):
    """Search game tree to determine best move; return (value, move) pair."""

    player = state.to_move

    def max_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a))
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)

infinity = math.inf

def alphabeta_search(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    def max_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)



def cache1(function):
    "Like lru_cache(None), but only considers the first argument of function."
    cache = {}
    def wrapped(x, *args):
        if x not in cache:
            cache[x] = function(x, *args)
        return cache[x]
    return wrapped


def alphabeta_search_tt(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    @cache1
    def max_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda game, state, depth: depth > d

def h_alphabeta_search(game, state, cutoff=cutoff_depth(2)):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    @cache1
    def max_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta, depth+1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity, 0)

import itertools

def h(board, player):
    punteggio = 0

    # 1. Valore dei dadi
    punteggio += calcola_valore_dadi(board, player)

    # 2. Controllo del centro
    punteggio += controllo_centro(board)

    # 3. Potenziale di cattura
    punteggio += calcola_punteggio_cattura(board, player)

    # 4. Penalizzazione per posizioni vulnerabili
    punteggio -= calcola_posizioni_vulnerabili(board, player)

    # 5. Valore dei dadi alti
    punteggio += calcola_valori_dadi_alti(board, player)

    return punteggio


def calcola_valore_dadi(board, player):
    valore_dadi = 0
    for riga in board.board:
        for dado in riga:
            if dado is not None:
                if dado[0] == player:
                    valore_dadi += dado[1]
                else:
                    valore_dadi -= dado[1]
    return valore_dadi


def controllo_centro(board):
    centro_punteggio = 0
    mid = board.size // 2
    if board.board[mid][mid] is None:
        centro_punteggio += 100
    return centro_punteggio


def calcola_punteggio_cattura(board, player):
    punteggio_bonus = 0
    max_bonus = 0

    for i in range(board.size):
        for j in range(board.size):
            cella = board.board[i][j]
            if cella is not None:
                catture = valuta_cattura(board, i, j)
                for somma, mosse in catture.items():
                    for mossa in mosse:
                        if mossa["punteggio"] > max_bonus:
                            max_bonus = mossa["punteggio"]

    punteggio_bonus += max_bonus
    return punteggio_bonus


def valuta_cattura(board, r, c):
    adiacenti = [
        ((nr, nc), board.board[nr][nc][1])
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 0 <= (nr := r + dr) < board.size
        and 0 <= (nc := c + dc) < board.size
        and board.board[nr][nc] is not None
    ]

    if len(adiacenti) < 2:
        return {}

    punteggi = {6: 20, 5: 18, 4: 16, 3: 14, 2: 12}
    catture = {}
    visti = set()

    for r_size in range(2, len(adiacenti) + 1):
        for subset in itertools.combinations(adiacenti, r_size):
            celle = tuple(sorted(pos for pos, _ in subset))
            somma = sum(pip for _, pip in subset)
            if 2 <= somma <= 6 and celle not in visti:
                visti.add(celle)
                catture.setdefault(somma, []).append({
                    "bersaglio": (r, c),
                    "celle_coinvolte": celle,
                    "punteggio": punteggi[somma]
                })

    return catture


def calcola_posizioni_vulnerabili(board, player):
    punteggio = 0
    for i in range(board.size):
        for j in range(board.size):
            cella = board.board[i][j]
            if cella is not None and cella[0] == player:
                if is_vulnerable(board.board, i, j, player):
                    punteggio += 5  # Penalità per ogni dado vulnerabile
    return punteggio


def is_vulnerable(board_array, i, j, player):
    avversario = 1 if player == 2 else 2
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(board_array) and 0 <= nj < len(board_array[0]):
            vicino = board_array[ni][nj]
            if vicino is not None and vicino[0] == avversario:
                return True
    return False


def calcola_valori_dadi_alti(board, player):
    punteggio = 0
    for riga in board.board:
        for dado in riga:
            if dado is not None and dado[0] == player and dado[1] > 5:
                punteggio += dado[1]
    return punteggio
