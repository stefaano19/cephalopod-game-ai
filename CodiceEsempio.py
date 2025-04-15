def h(board, player):
    """
    Implementa l'euristica per la valutazione della posizione sulla scacchiera.
    """
    punteggio = 0
    
    # Parametri per il controllo del centro (ad esempio, per una griglia 8x8, le posizioni centrali sono 3-4, 3-5, 4-3, 4-4)
    centro_posizioni = [(3, 3), (3, 4), (4, 3), (4, 4)]
    
    # Calcolare il punteggio in base al controllo del centro
    centro_punteggio = 0
    for pos in centro_posizioni:
        if board[pos[0]][pos[1]] == player:  # Se il dado del giocatore è nelle posizioni centrali
            centro_punteggio += 5  # Incremento per il controllo del centro
    punteggio += centro_punteggio
    
    # Calcolare il punteggio in base ai valori dei dadi
    valore_dadi = 0
    for riga in board:
        for dado in riga:
            if dado == player:
                valore_dadi += 3  # Aggiungiamo un punteggio per ogni dado del giocatore
            elif dado != 0:  # Se c'è un dado dell'avversario
                valore_dadi -= 2  # Penalizziamo l'avversario

    punteggio += valore_dadi

    # Catture vantaggiose (supponiamo che catturare un dado avversario aumenti il punteggio di 10)
    catture_punteggio = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0 and board[i][j] != player:  # Dado dell'avversario
                if is_capturable(board, i, j, player):  # Funzione che verifica se la posizione può essere catturata
                    catture_punteggio += 10  # Incremento per catture vantaggiose

    punteggio += catture_punteggio

    # Posizioni vulnerabili: penalizziamo il giocatore se mette dadi in posizioni che potrebbero essere catturate facilmente
    vulnerabilità_punteggio = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == player:  # Dado del giocatore
                if is_vulnerable(board, i, j, player):  # Funzione che verifica se la posizione è vulnerabile
                    vulnerabilità_punteggio -= 5  # Penalizziamo le posizioni vulnerabili

    punteggio += vulnerabilità_punteggio
    
    return punteggio

def is_capturable(board, i, j, player):
    """
    Funzione che determina se un dado può essere catturato.
    (Si assume che ci sia una logica per determinare se una cella può essere catturata.)
    """
    # Logica per verificare se un dado è vulnerabile (esempio: se una cella è adiacente a un dado nemico)
    # Questo dipenderà dalla regola del gioco, che non è specificata, quindi la logica qui è solo esemplificativa.
    return False  # Placeholder, da implementare in base alle regole specifiche

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
