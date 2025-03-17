# Tic-Tac-Toe Spiel für zwei Spieler
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board):
    # Reihen und Spalten prüfen
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != " ":
            return board[0][i]
    
    # Diagonalen prüfen
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    
    return None

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    player = "X"
    
    while True:
        print_board(board)
        print(f"Spieler {player} ist dran.")
        
        try:
            row, col = map(int, input("Gib deine Position als 'Zeile Spalte' (0-2) ein: ").split())
            if board[row][col] != " ":
                print("Das Feld ist bereits belegt! Versuch es erneut.")
                continue
        except (ValueError, IndexError):
            print("Ungültige Eingabe. Bitte gib zwei Zahlen zwischen 0 und 2 ein.")
            continue
        
        board[row][col] = player
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Spieler {winner} gewinnt!")
            break
        if is_full(board):
            print_board(board)
            print("Unentschieden!")
            break
        
        player = "O" if player == "X" else "X"

# Starte das Spiel
tic_tac_toe()
