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
    punteggio += 0.5 * controllo_centro(board)
    punteggio += calcola_valore_dadi(board, player)
    punteggio += 0.8 * calcola_punteggio_cattura(board, player)
    #punteggio += calcola_mobilita(board, player)

    # Defensive aspect: Penalize vulnerable positions
    penalty_vulnerable = 0
    if hasattr(board, 'board') and hasattr(board, 'size'):
        for r in range(board.size):
            for c in range(board.size):
                dado = board.board[r][c]
                if dado is not None and dado[0] == player:
                    if is_vulnerable(board.board, r, c, player):
                        penalty_vulnerable += 5  # Adjust the penalty value as needed
    elif isinstance(board, list): # Assuming a raw board state is passed
        size = len(board)
        for r in range(size):
            for c in range(size):
                dado = board[r][c]
                if dado is not None and dado[0] == player:
                    if is_vulnerable(board, r, c, player):
                        penalty_vulnerable += 5

    punteggio -= penalty_vulnerable
    return punteggio

def calcola_valore_dadi(board, player):
    valore_dadi = 0
    if hasattr(board, 'board'):
        game_board = board.board
    elif isinstance(board, list):
        game_board = board
    else:
        return 0

    for riga in game_board:
        for dado in riga:
            if dado is not None:
                if dado[0] == player:
                    valore_dadi += dado[1]
                else:
                    valore_dadi -= dado[1]
    return valore_dadi


def controllo_centro(board):
    centro_punteggio=0
    if hasattr(board, 'board') and hasattr(board, 'size') and 0 <= 2 < board.size and 0 <= 2 < board.size:
        if board.board[2][2] is None:
            centro_punteggio += 100
    elif isinstance(board, list) and len(board) > 2 and len(board[2]) > 2:
        if board[2][2] is None:
            centro_punteggio += 100
    return centro_punteggio

def calcola_mobilita(state, player):
    """
    Calcola quante celle vuote sono adiacenti a uno dei dadi del giocatore,
    ovvero dove potrebbe muoversi.
    """
    mobilita = set()
    if hasattr(state, 'board') and hasattr(state, 'size'):
        board = state.board
        size = state.size
        for i in range(size):
            for j in range(size):
                if board[i][j] is not None and board[i][j][0] == player:
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < size and 0 <= nj < size and board[ni][nj] is None:
                            mobilita.add((ni, nj))
    elif isinstance(state, list): # Assuming state is just the board
        size = len(state)
        board = state
        for i in range(size):
            for j in range(size):
                if board[i][j] is not None and board[i][j][0] == player:
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < size and 0 <= nj < size and board[ni][nj] is None:
                            mobilita.add((ni, nj))
    elif hasattr(state, 'board'):
        board = state.board
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
    punteggio_bonus = 0
    max_bonus = 0
    game_board = None
    size = 0

    if hasattr(board, 'board') and hasattr(board, 'size'):
        game_board = board.board
        size = board.size
    elif isinstance(board, list):
        game_board = board
        size = len(board)
    else:
        return 0

    for i in range(size):
        for j in range(size):
            cella = game_board[i][j]
            if cella is not None:
                catture = valuta_cattura(board, i, j)
                for somma, mosse in catture.items():
                    for mossa in mosse:
                        if mossa["punteggio"] > max_bonus:
                            max_bonus = mossa["punteggio"]

    punteggio_bonus += max_bonus
    return punteggio_bonus


def valuta_cattura(board_or_state, r, c):
    game_board = None
    size = 0
    if hasattr(board_or_state, 'board') and hasattr(board_or_state, 'size'):
        game_board = board_or_state.board
        size = board_or_state.size
    elif isinstance(board_or_state, list):
        game_board = board_or_state
        size = len(board_or_state)
    else:
        return {}

    adiacenti = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size and game_board[nr][nc] is not None:
            adiacenti.append(((nr, nc), game_board[nr][nc][1]))

    if len(adiacenti) < 2:
        return {}

    punteggi = {6: 20, 5: 15, 4: 16, 3: 14, 2: 12}
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
    """
    Determines if a die at (r, c) belonging to 'player' is vulnerable
    to capture by the opponent.
    """
    if not board_state:
        return False
    opponent = 1 if player == 2 else 2
    size = len(board_state)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size and board_state[nr][nc] is not None and board_state[nr][nc][0] == opponent:
            # For a simpler vulnerability check, we just see if an opponent's die is adjacent.
            return True
    return False

def calcola_valori_dadi_alti(stato):
    punteggio = 0
    board = None
    if hasattr(stato, 'board'):
        board = stato.board
    elif isinstance(stato, list):
        board = stato
    else:
        return 0

    for riga in board:
        for cella in riga:
            if isinstance(cella, tuple) and len(cella) == 2:
                valore_dado = cella[1]
                if valore_dado > 5:
                    punteggio += valore_dado
    return punteggio