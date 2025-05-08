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
    peso_centro=0.4
    peso_cattura=1.2
    peso_vulnerabilita=8.0
   
    punteggio = 0
    punteggio += peso_centro * controllo_centro(board, player)
    punteggio += calcola_valore_dadi(board, player)
    punteggio += peso_cattura * calcola_punteggio_cattura(board, player)
    #punteggio += peso_mobilita * calcola_mobilita(board, player)
    #punteggio += peso_futuro * potenziale_cattura_futura(board, player)
    
    penalty_vulnerable = calcola_vulnerabilita_ottimizzata(board, player, peso_vulnerabilita)
    punteggio -= penalty_vulnerable

    
    return punteggio

def calcola_valore_dadi(board, player):
    valore_dadi = 0
    game_board = board.board if hasattr(board, 'board') else board
    if not game_board:
        return 0
    for riga in game_board:
        for dado in riga:
            if dado is not None:
                val = dado[1]
                if dado[0] == player:
                    valore_dadi += 1.1 * val
                else:
                    valore_dadi -= val
    return valore_dadi


def controllo_centro(board, player):
    size = board.size if hasattr(board, 'size') else (len(board) if isinstance(board, list) else 0)
    if size > 0 and 0 <= size // 2 < size:
        r_centro, c_centro = size // 2, size // 2
        game_board = board.board if hasattr(board, 'board') else board
        if game_board:
            cella_centro = game_board[r_centro][c_centro]
            if cella_centro is None:
                return 10
            elif cella_centro[0] != player:
                return -5
    return 0


def calcola_mobilita(state, player):
    mobilita = set()
    board = state.board if hasattr(state, 'board') else state
    if not board:
        return 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] is not None and board[i][j][0] == player:
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < size and 0 <= nj < size and board[ni][nj] is None:
                        mobilita.add((ni, nj))
    return len(mobilita)

def calcola_punteggio_cattura(board, player):
    max_bonus = 0
    game_board = board.board if hasattr(board, 'board') else board
    if not game_board:
        return 0
    size = len(game_board)
    for i in range(size):
        for j in range(size):
            if game_board[i][j] is not None:
                catture = valuta_cattura(board, i, j)
                for mosse in catture.values():
                    for mossa in mosse:
                        max_bonus = max(max_bonus, mossa["punteggio"])
    return max_bonus

def valuta_cattura(board_or_state, r, c):
    game_board = board_or_state.board if hasattr(board_or_state, 'board') else board_or_state
    if not game_board:
        return {}
    size = len(game_board)
    adiacenti = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size and game_board[nr][nc] is not None:
            adiacenti.append(((nr, nc), game_board[nr][nc][1]))

    if len(adiacenti) < 2:
        return {}

    punteggi = {6: 20, 5: 18, 4: 16, 3: 14, 2: 12}
    catture = {}
    visti = set()

    for r_size in range(2, len(adiacenti) + 1):
        for subset in itertools.combinations(adiacenti, r_size):
            celle = tuple(sorted(pos for pos, _ in subset))
            somma = sum(pip for _, pip in subset)
            if somma == 6: 
                catture.setdefault(somma, []).append({
                    "bersaglio": (r, c),
                    "celle_coinvolte": celle,
                    "punteggio": punteggi.get(somma, 0)
                })
                break
            if 2 <= somma <= 6 and celle not in visti:
                visti.add(celle)
                catture.setdefault(somma, []).append({
                    "bersaglio": (r, c),
                    "celle_coinvolte": celle,
                    "punteggio": punteggi.get(somma, 0)
                })
    return catture

def calcola_vulnerabilita_ottimizzata(board, player, peso_vulnerabilita):
    penalty_vulnerable = 0
    game_board = board.board if hasattr(board, 'board') else board
    if not game_board:
        return 0
    size = len(game_board)
    opponent = 1 if player == 2 else 2
    for r in range(size):
        for c in range(size):
            dado = game_board[r][c]
            if dado is not None and dado[0] == player:
                dado_valore = dado[1]
                vulnerability_score = 0
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < size and 0 <= nc < size:
                        vicino = game_board[nr][nc]
                        if vicino is not None and vicino[0] == opponent:
                            vulnerability_score += vicino[1]
                if vulnerability_score >= dado_valore:
                    penalty_vulnerable += peso_vulnerabilita
    return penalty_vulnerable


def calcola_valori_dadi_alti(stato):
    punteggio = 0
    board = stato.board if hasattr(stato, 'board') else stato
    if not board:
        return 0
    for riga in board:
        for cella in riga:
            if isinstance(cella, tuple) and len(cella) == 2 and cella[1] > 5:
                punteggio += cella[1]
    return punteggio