import itertools
import math

from CephalopodGame import get_subsets

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

def h(board, player):
    """
    Implementa l'euristica per la valutazione della posizione sulla scacchiera.
    """
    punteggio = 0

    return punteggio

def calcola_valore_dadi(board, player):
    valore_dadi = 0
    for riga in board.board:
        for dado in riga:
            if dado is not None:
                if dado[0] == player:
                    valore_dadi += dado[1]  # aggiungi i pip dei tuoi dadi
                else:
                    valore_dadi -= dado[1]  # togli i pip degli avversari
    return valore_dadi


def controllo_centro(board):
    centro_punteggio=0
    if board.board[2][2]==None:
        centro_punteggio +=100
    return centro_punteggio

"""def calcola_punteggio_cattura(board, player):
    # mappa della somma pip → punteggio
    punteggi = {
        6: 20,
        5: 16,
        4: 14,
        3: 12,
        2: 10
    }

    punteggio_bonus = 0

    for i in range(board.size):
        for j in range(board.size):
            cella = board.board[i][j]
            if cella is not None and cella[0] != player:
                mosse = valuta_cattura(board, i, j)
                for somma, pos in mosse.items():
                    if somma in punteggi:
                        punteggio_bonus += punteggi[somma]

    return punteggio_bonus

    """
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




""" def valuta_cattura(board, r, c):
    pip_adiacenti = [
        board.board[nr][nc][1]
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 0 <= (nr := r + dr) < board.size
        and 0 <= (nc := c + dc) < board.size
        and board.board[nr][nc] is not None
    ]

    if len(pip_adiacenti) < 2:
        return None

    somma_massima = 0
    for r_size in range(2, len(pip_adiacenti) + 1):
        for subset in itertools.combinations(pip_adiacenti, r_size):
            somma = sum(subset)
            if 2 <= somma <= 6 and somma > somma_massima:
                somma_massima = somma

    if somma_massima > 0:
        return (r, c), somma_massima

    return None """


def valuta_cattura(board, r, c):
    # Ottieni pip adiacenti con le loro coordinate
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
    visti = set()  # Per evitare duplicati

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


def calcola_posizioni_vulnerabili(stato):
    # Penalizza le mosse che mettono i dadi in posizioni vulnerabili
    punteggio = 0
    # Logica per trovare posizioni vulnerabili
    return punteggio

def is_vulnerable(board, i, j, player):
    """
    Funzione che determina se un dado è vulnerabile a una cattura dell'avversario.
    """
    # Controlla le posizioni adiacenti per verificare se l'avversario può catturare il dado
    avversario = 1 if player == 2 else 2  # Se il giocatore è 1, l'avversario è 2, e viceversa
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(board) and 0 <= nj < len(board[0]) and board[ni][nj] == avversario:
            return True
    return False

def calcola_valori_dadi_alti(stato):
    # Premia i dadi con valori alti sulla scacchiera
    punteggio = 0
    for riga in stato:
        for dado in riga:
            if dado > 5:  # Dadi con valore maggiore di 5 sono considerati forti
                punteggio += dado
    return punteggio

