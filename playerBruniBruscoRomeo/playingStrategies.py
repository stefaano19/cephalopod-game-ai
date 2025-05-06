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
    punteggio = 0
    punteggio += 0.3 * controllo_centro(board)
    punteggio += calcola_valore_dadi(board, player)
    punteggio += 1.2 * calcola_punteggio_cattura(board, player)

    # Aspetto difensivo potenziato:
    penalty_vulnerable = 0
    if hasattr(board, 'board') and hasattr(board, 'size'):
        for r in range(board.size):
            for c in range(board.size):
                dado = board.board[r][c]
                if dado is not None and dado[0] == player:
                    if is_vulnerable(board.board, r, c, player):
                        penalty_vulnerable += 8
    elif isinstance(board, list):
        size = len(board)
        for r in range(size):
            for c in range(size):
                dado = board[r][c]
                if dado is not None and dado[0] == player:
                    if is_vulnerable(board, r, c, player):
                        penalty_vulnerable += 8

    punteggio -= penalty_vulnerable

    # Mobilità
    if hasattr(board, 'size'):
        try:
            # Assumendo che 'calcola_mobilita' accetti 'board' e 'player'
            punteggio += 0.5 * calcola_mobilita(board, player)
        except Exception as e:
            print(f"Errore nel calcolo della mobilità: {e}")

    return punteggio

def calcola_valore_dadi(board, player):
    valore_dadi = 0
    game_board = getattr(board, 'board', board if isinstance(board, list) else None)
    if game_board:
        for riga in game_board:
            for dado in riga:
                if dado is not None:
                    valore_dadi += dado[1] if dado[0] == player else -dado[1]
    return valore_dadi


def controllo_centro(board):
    centro_punteggio = 0
    game_board = getattr(board, 'board', board if isinstance(board, list) else None)
    size = getattr(board, 'size', len(game_board) if isinstance(game_board, list) else 0)
    if game_board and size > 2 and len(game_board[2]) > 2:
        if game_board[2][2] is None:
            centro_punteggio += 100
    return centro_punteggio

def calcola_mobilita(state, player):
    """
    Calcola quante celle vuote sono adiacenti a uno dei dadi del giocatore.
    """
    mobilita = set()
    board = getattr(state, 'board', state if isinstance(state, list) else None)
    size = getattr(state, 'size', len(board) if isinstance(board, list) else 0)
    if board:
        for r in range(size):
            for c in range(size):
                if board[r][c] is not None and board[r][c][0] == player:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < size and 0 <= nc < size and board[nr][nc] is None:
                            mobilita.add((nr, nc))
    return len(mobilita)


def calcola_punteggio_cattura(board, player):
    punteggio_bonus = 0
    max_bonus = 0
    game_board = getattr(board, 'board', board if isinstance(board, list) else None)
    size = getattr(board, 'size', len(game_board) if isinstance(game_board, list) else 0)

    if game_board:
        for r in range(size):
            for c in range(size):
                cella = game_board[r][c]
                if cella is not None:
                    catture = valuta_cattura(board, r, c)
                    for _, mosse in catture.items():
                        for mossa in mosse:
                            max_bonus = max(max_bonus, mossa.get("punteggio", 0))
    punteggio_bonus += max_bonus
    return punteggio_bonus


def valuta_cattura(board_or_state, r, c):
    game_board = getattr(board_or_state, 'board', board_or_state if isinstance(board_or_state, list) else None)
    size = len(game_board) if isinstance(game_board, list) else getattr(board_or_state, 'size', 0)
    if not game_board:
        return {}

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
            if 2 <= somma <= 6 and celle not in visti:
                visti.add(celle)
                catture.setdefault(somma, []).append({
                    "bersaglio": (r, c),
                    "celle_coinvolte": celle,
                    "punteggio": punteggi.get(somma, 0)
                })
    return catture

def is_vulnerable(board_state, r, c, player):
    if not board_state:
        return False
    opponent = 1 if player == 2 else 2
    size = len(board_state)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size and board_state[nr][nc] is not None and board_state[nr][nc][0] == opponent:
            return True
    return False

def calcola_valori_dadi_alti(stato):
    punteggio = 0
    board = getattr(stato, 'board', stato if isinstance(stato, list) else None)
    if board:
        for riga in board:
            for cella in riga:
                if isinstance(cella, tuple) and len(cella) == 2:
                    valore_dado = cella[1]
                    if valore_dado > 5:
                        punteggio += valore_dado
    return punteggio