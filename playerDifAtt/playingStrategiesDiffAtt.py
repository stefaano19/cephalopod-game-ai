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


def h(board, player):
    return h_potenziata(board, player)

def h_potenziata(board, player):
    tuoi = conta_dadi(board, player)
    nemici = sum(1 for r in board.board for c in r if c is not None and c[0] != player)
    differenza = tuoi - nemici
    valore_dadi = calcola_valore_dadi(board, player)

    # Peso aggressività aumenta se sei sotto
    peso_aggressivita = normalizza(-differenza, -24, 24)  # più sei sotto, più cresce
    peso_difesa = normalizza(differenza, -24, 24)          # più sei avanti, più cresce
    peso_equilibrio = 1.0 - abs(normalizza(differenza, -24, 24))

    # Valutazione combinata con ponderazione dinamica
    return (
        h_aggressiva(board, player) * peso_aggressivita +
        h_difensiva(board, player) * peso_difesa +
        h_equilibrata(board, player) * peso_equilibrio
    )

def h_equilibrata(board, player):
    return (
        normalizza(controllo_centro(board), 0, 100) * 1.3 +
        normalizza(calcola_valore_dadi(board, player), -30, 30) * 1.2 +
        normalizza(calcola_punteggio_cattura(board, player), 0, 80) * 1.3 +
        normalizza(calcola_posizioni_vulnerabili(board, player), -24, 0) * 1.2 +
        normalizza(calcola_valori_dadi_alti(board), 0, 24) * 1.1 +
        normalizza(pressione_board(board, player), -10, 10) * 1.0 +
        normalizza(conta_dadi(board, player), 0, 24) * 1.0 +
        normalizza(calcola_supporto_alleati(board, player), 0, 20) * 1.0 +
        normalizza(controllo_bordi(board, player), -24, 0) * 1.0
    )

def h_aggressiva(board, player):
    return (
        normalizza(controllo_centro(board), 0, 100) * 1.2 +
        normalizza(calcola_valore_dadi(board, player), -30, 30) * 1.5 +
        normalizza(calcola_punteggio_cattura(board, player), 0, 80) * 1.6 +
        normalizza(calcola_posizioni_vulnerabili(board, player), -24, 0) * 0.5 +
        normalizza(calcola_valori_dadi_alti(board), 0, 24) * 1.3 +
        normalizza(pressione_board(board, player), -10, 10) * 1.1 +
        normalizza(conta_dadi(board, player), 0, 24) * 0.5 +
        normalizza(calcola_supporto_alleati(board, player), 0, 20) * 0.4 +
        normalizza(controllo_bordi(board, player), -24, 0) * 0.5
    )

def h_difensiva(board, player):
    return (
        normalizza(controllo_centro(board), 0, 100) * 1.5 +
        normalizza(calcola_valore_dadi(board, player), -30, 30) * 1.0 +
        normalizza(calcola_punteggio_cattura(board, player), 0, 80) * 0.7 +
        normalizza(calcola_posizioni_vulnerabili(board, player), -24, 0) * 1.6 +
        normalizza(calcola_valori_dadi_alti(board), 0, 24) * 1.0 +
        normalizza(pressione_board(board, player), -10, 10) * 0.8 +
        normalizza(conta_dadi(board, player), 0, 24) * 1.2 +
        normalizza(calcola_supporto_alleati(board, player), 0, 20) * 1.3 +
        normalizza(controllo_bordi(board, player), -24, 0) * 1.5
    )

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

    punteggi = {6: 40, 5: 28, 4: 36, 3: 28, 2: 24}
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


def is_vulnerable(board, i, j, player):
    """
    Restituisce True se la cella (i, j) contiene un dado del giocatore
    ed è adiacente a uno o più dadi dell'avversario.
    """
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < board.size and 0 <= nj < board.size:
            neighbor = board.board[ni][nj]
            if neighbor is not None and neighbor[0] != player:
                return True
    return False

def calcola_posizioni_vulnerabili(board, player):
    """
    Penalizza le posizioni in cui il giocatore ha dadi vulnerabili,
    restituendo un punteggio negativo.
    """
    punteggio = 0

    for i in range(board.size):
        for j in range(board.size):
            cella = board.board[i][j]
            if cella is not None and cella[0] == player:
                if (i, j) == (2, 2):
                    continue  # non penalizziamo il centro
                if cella[1] > 5:
                    continue  # non penalizziamo dadi forti
                if is_vulnerable(board, i, j, player):
                    penalita = cella[1]  # penalizza in base al valore del dado
                    punteggio -= penalita
    return punteggio


def calcola_valori_dadi_alti(board):
    # Premia i dadi con valori alti sulla scacchiera
    punteggio = 0
    for riga in board.board:
        for dado in riga:
            if dado is not None:
                if dado[1] > 5:  # Dadi con valore maggiore di 5 sono considerati forti
                    punteggio += dado[1]
    return punteggio


def conta_dadi(board, player):
    return sum(1 for row in board.board for cell in row if cell is not None and cell[0] == player)

def pressione_board(board, player):
    count_player = sum(1 for r in board.board for c in r if c is not None and c[0] == player)
    count_enemy = sum(1 for r in board.board for c in r if c is not None and c[0] != player)
    return (count_player - count_enemy) * 2


def normalizza(valore, minimo, massimo):
    if massimo == minimo:
        return 0
    return (valore - minimo) / (massimo - minimo) * 2 - 1  # scala tra -1 e +1



def calcola_supporto_alleati(board, player):
    punteggio = 0
    for i in range(board.size):
        for j in range(board.size):
            cella = board.board[i][j]
            if cella is not None and cella[0] == player:
                alleati_vicini = 0
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < board.size and 0 <= nj < board.size:
                        vicino = board.board[ni][nj]
                        if vicino is not None and vicino[0] == player:
                            alleati_vicini += 1
                punteggio += alleati_vicini
    return punteggio

def controllo_bordi(board, player):
    """
    Penalizza la presenza di dadi del giocatore sulle caselle dei bordi della scacchiera.
    Restituisce un punteggio negativo maggiore per ogni dado posizionato su una casella di bordo.
    """
    penalita_bordi = 0
    for i in [0, board.size - 1]:  # Prima e ultima riga
        for j in range(board.size):
            dado = board.board[i][j]
            if dado is not None and dado[0] == player:
                penalita_bordi -= dado[1]  # Penalizza in base al valore del dado
    for j in [0, board.size - 1]:  # Prima e ultima colonna
        for i in range(1, board.size - 1):  # Evita di contare gli angoli due volte
            dado = board.board[i][j]
            if dado is not None and dado[0] == player:
                penalita_bordi -= dado[1]  # Penalizza in base al valore del dado
    return penalita_bordi
