import streamlit as st
from typing import Literal

class King:
    def __init__(self, color: Literal["black", "white"]) -> None:
        self.color = color
        self.is_checked: bool = False
        self.has_legal_moves = False
        self.icon = "♔" if self.color == "white" else "♚"
        self.key = f"{self.color}_king"

    def is_in_check(self, board):
            king_x, king_y = self.find_king_position(board)
            enemy_color = "black" if self.color == "white" else "white"

            for i in range(8):
                for j in range(8):
                    piece = board[i][j].piece
                    if piece and piece.color == enemy_color:
                        if isinstance(piece, Pawn):
                            if (king_x, king_y) in piece.get_attack_squares(i, j):
                                return True
                        elif (king_x, king_y) in piece.get_attack_squares(board, i, j):
                            return True
            return False

    def find_king_position(self, board):
        for i in range(8):
            for j in range(8):
                piece = board[i][j].piece
                if isinstance(piece, King) and piece.color == self.color:
                    return i, j
        return None, None

    def move_rescues_king(self, board, from_x, from_y, to_x, to_y):
        temp_piece = board[to_x][to_y].piece
        board[to_x][to_y].piece = board[from_x][from_y].piece
        board[from_x][from_y].piece = None

        is_in_check = board.is_king_in_check()  # Check if the move rescues the king

        # Revert move
        board[from_x][from_y].piece = board[to_x][to_y].piece
        board[to_x][to_y].piece = temp_piece

        return not is_in_check

    def is_square_under_attack(self, board, x, y, my_color):
        for i in range(8):
            for j in range(8):
                piece = board[i][j].piece
                if piece and piece.color != my_color:
                    # Skip the king
                    if isinstance(piece, King):
                        continue
                    elif isinstance(piece, Pawn):
                        if (x, y) in piece.get_attack_squares(i, j):
                            return True
                    elif (x, y) in piece.get_attack_squares(board, i, j):
                        return True
        return False

    def is_protected(self, board, x, y, my_color):
        for i in range(8):
            for j in range(8):
                piece = board[i][j].piece
                if piece and piece.color != my_color:  # Skip my pieces
                    if isinstance(piece, King):
                        continue
                    elif isinstance(piece, Pawn):
                        if (x, y) in piece.get_attack_squares(i, j):
                            return True
                    elif (x, y) in piece.get_attack_squares(board, i, j):
                        return True
        return False

    def get_moves(self, board, x, y):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < 8 and 0 <= new_y < 8:
                if not self.is_square_under_attack(board, new_x, new_y, self.color):
                    target_piece = board[new_x][new_y].piece
                    if target_piece:
                        if target_piece.color != self.color and not self.is_protected(board, new_x, new_y, self.color):
                            moves.append((new_x, new_y))
                    else:
                        moves.append((new_x, new_y))

        st.session_state.all_legal_moves.extend(moves)
        return moves
    
    def get_attack_squares(self, board, x, y):
        moves = []

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < 8 and 0 <= new_y < 8:
                moves.append((new_x, new_y))

        return moves

class Queen:
    def __init__(self, color: Literal["black", "white"], index: int) -> None:
        self.color = color
        self.has_legal_moves: bool = False
        self.icon = "♕" if self.color == "black" else "♛"
        self.key = f"{self.color}_queen_{index}"

    def get_moves(self, board, x, y):
        moves = []

        # Directions for queen: horizontal, vertical and diagonal
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i

                # Check board boundaries
                if new_x < 0 or new_x >= 8 or new_y < 0 or new_y >= 8:
                    break

                # Check for presence of another piece
                if board[new_x][new_y].piece:
                    # If it's an opponent's piece, add the move and stop
                    if board[new_x][new_y].piece.color != self.color:
                        moves.append((new_x, new_y))
                    break
                else:
                    # Add moves if not blocked
                    moves.append((new_x, new_y))

        st.session_state.all_legal_moves.extend(moves)
        return moves
    
    def get_attack_squares(self, board, x, y):
        moves = []

        # Directions for queen: horizontal, vertical and diagonal
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i

                # Check board boundaries
                if new_x < 0 or new_x >= 8 or new_y < 0 or new_y >= 8:
                    break

                # Check for presence of another piece
                if board[new_x][new_y].piece:
                    # If it's an opponent's piece, add the move and stop
                    moves.append((new_x, new_y))
                    break
                else:
                    # Add moves if not blocked
                    moves.append((new_x, new_y))

        return moves

class Bishop:
    def __init__(self, color: Literal["black", "white"], index: int) -> None:
        self.color = color
        self.has_legal_moves: bool = False
        self.icon = "♗" if self.color == "black" else "♝"
        self.key = f"{self.color}_bishop_{index}"

    def get_moves(self, board, x, y):
        moves = []

        # All four diagonals
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i

                # Check board boundaries
                if new_x < 0 or new_x >= 8 or new_y < 0 or new_y >= 8:
                    break

                # Check for presence of another piece
                if board[new_x][new_y].piece:
                    # If it's an opponent's piece, add the move and stop
                    if board[new_x][new_y].piece.color != self.color:
                        moves.append((new_x, new_y))
                    break
                else:
                    # Add moves if not blocked
                    moves.append((new_x, new_y))

        st.session_state.all_legal_moves.extend(moves)
        return moves
    
    def get_attack_squares(self, board, x, y):
        moves = []

        # All four diagonals
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i

                # Check board boundaries
                if new_x < 0 or new_x >= 8 or new_y < 0 or new_y >= 8:
                    break

                # Check for presence of another piece
                if board[new_x][new_y].piece:
                    # If it's an opponent's piece, add the move and stop
                    moves.append((new_x, new_y))
                    break
                else:
                    # Add moves if not blocked
                    moves.append((new_x, new_y))

        return moves
            
class Knight:
    def __init__(self, color: Literal["black", "white"], index: int) -> None:
        self.color = color
        self.has_legal_moves: bool = True
        self.icon = "♘" if self.color == "black" else "♞"
        self.key = f"{self.color}_knight_{index}"

    def get_moves(self, board, x, y):
        moves = []

        try:
            if board[x+2][y+1].piece:
                if board[x+2][y+1].piece.color != self.color:
                    moves.append((x+2, y+1))
            else:
                moves.append((x+2, y+1))
        except IndexError: pass

        try:
            if board[x+1][y+2].piece:
                if board[x+1][y+2].piece.color != self.color:
                    moves.append((x+1, y+2))
            else:
                moves.append((x+1, y+2))
        except IndexError: pass

        try:
            if x-2 < 0 or y-1 < 0: raise IndexError
            if board[x-2][y-1].piece:
                if board[x-2][y-1].piece.color != self.color:
                    moves.append((x-2, y-1))
            else:
                moves.append((x-2, y-1))
        except IndexError: pass

        try:
            if x-1 < 0 or y-2 < 0: raise IndexError
            if board[x-1][y-2].piece:
                if board[x-1][y-2].piece.color != self.color:
                    moves.append((x-1, y-2))
            else:
                moves.append((x-1, y-2))
        except IndexError: pass

        try:
            if y-1 < 0: raise IndexError
            if board[x+2][y-1].piece:
                if board[x+2][y-1].piece.color != self.color:
                    moves.append((x+2, y-1))
            else:
                moves.append((x+2, y-1))
        except IndexError: pass

        try:
            if y-2 < 0: raise IndexError
            if board[x+1][y-2].piece:
                if board[x+1][y-2].piece.color != self.color:
                    moves.append((x+1, y-2))
            else:
                moves.append((x+1, y-2))	
        except IndexError: pass

        try:
            if x-2 < 0: raise IndexError
            if board[x-2][y+1].piece:
                if board[x-2][y+1].piece.color != self.color:
                    moves.append((x-2, y+1))
            else:
                moves.append((x-2, y+1))
        except IndexError: pass

        try:
            if x-1 < 0: raise IndexError
            if board[x-1][y+2].piece:
                if board[x-1][y+2].piece.color != self.color:
                    moves.append((x-1, y+2))
            else:
                moves.append((x-1, y+2))
        except IndexError: pass

        st.session_state.all_legal_moves.extend(moves)
        return moves

    def get_attack_squares(self, board, x, y):
        moves = []

        try:
            if board[x+2][y+1].piece:
                moves.append((x+2, y+1))
            else:
                moves.append((x+2, y+1))
        except IndexError: pass

        try:
            if board[x+1][y+2].piece:
                moves.append((x+1, y+2))
            else:
                moves.append((x+1, y+2))
        except IndexError: pass

        try:
            if x-2 < 0 or y-1 < 0: raise IndexError
            if board[x-2][y-1].piece:
                moves.append((x-2, y-1))
            else:
                moves.append((x-2, y-1))
        except IndexError: pass

        try:
            if x-1 < 0 or y-2 < 0: raise IndexError
            if board[x-1][y-2].piece:
                moves.append((x-1, y-2))
            else:
                moves.append((x-1, y-2))
        except IndexError: pass

        try:
            if y-1 < 0: raise IndexError
            if board[x+2][y-1].piece:
                moves.append((x+2, y-1))
            else:
                moves.append((x+2, y-1))
        except IndexError: pass

        try:
            if y-2 < 0: raise IndexError
            if board[x+1][y-2].piece:
                moves.append((x+1, y-2))
            else:
                moves.append((x+1, y-2))
        except IndexError: pass

        try:
            if x-2 < 0: raise IndexError
            if board[x-2][y+1].piece:
                moves.append((x-2, y+1))
            else:
                moves.append((x-2, y+1))
        except IndexError: pass

        try:
            if x-1 < 0: raise IndexError
            if board[x-1][y+2].piece:
                moves.append((x-1, y+2))
            else:
                moves.append((x-1, y+2))
        except IndexError: pass

        return moves

class Rook:
    def __init__(self, color: Literal["black", "white"], index) -> None:
        self.color = color
        self.has_legal_moves: bool = False
        self.icon = "♖" if self.color == "black" else "♜"
        self.key = f"{self.color}_rook_{index}"

    def get_moves(self, board, x, y):
        moves = []

        # Right
        for i in range(x+1, 8):
            try:
                if board[i][y].piece:
                    if board[i][y].piece.color == self.color: break
                    else:
                        moves.append((i, y))
                        break
                else:  moves.append((i, y))
            except IndexError: break

        # Left
        for i in range(x-1, -1, -1):
            try:
                if board[i][y].piece:
                    if board[i][y].piece.color == self.color: break
                    else:
                        moves.append((i, y))
                        break
                else:  moves.append((i, y))
            except IndexError: break

        # Up
        for i in range(y+1, 8):
            try:
                if board[x][i].piece:
                    if board[x][i].piece.color == self.color: break
                    else:
                        moves.append((x, i))
                        break
                else:  moves.append((x, i))
            except IndexError: break
        
        # Down
        for i in range(y-1, -1, -1):
            try:
                if board[x][i].piece:
                    if board[x][i].piece.color == self.color: break
                    else:
                        moves.append((x, i))
                        break
                else:  moves.append((x, i))
            except IndexError: break

        st.session_state.all_legal_moves.extend(moves)
        return moves
    
    def get_attack_squares(self, board, x, y):
        attack_squares = []

        # Right
        for i in range(x+1, 8):
            try:
                if board[i][y].piece:
                    attack_squares.append((i, y))
                    break
                else:  attack_squares.append((i, y))
            except IndexError: break

        # Left
        for i in range(x-1, -1, -1):
            try:
                if board[i][y].piece:
                    attack_squares.append((i, y))
                    break
                else:  attack_squares.append((i, y))
            except IndexError: break

        # Up
        for i in range(y+1, 8):
            try:
                if board[x][i].piece:
                    attack_squares.append((x, i))
                    break
                else:  attack_squares.append((x, i))
            except IndexError: break
        
        # Down
        for i in range(y-1, -1, -1):
            try:
                if board[x][i].piece:
                    attack_squares.append((x, i))
                    break
                else:  attack_squares.append((x, i))
            except IndexError: break

        return attack_squares

    
class Pawn:
    def __init__(self, color: Literal["black", "white"], index: int) -> None:
        self.color = color
        self.has_legal_moves: bool = True
        self.already_moved: bool = False
        self.icon = "♙" if self.color == "black" else "♟︎"
        self.key = f"{self.color}_pawn_{index}"

    def get_moves(self, board, x, y):	
        moves = []

        # WHITE
        # Forward
        if self.color == "white":
            if x < 8 and not board[x+1][y].piece:
                moves.append((x+1, y))
            # First move
            if not self.already_moved:
                if not board[x+1][y].piece and not board[x+2][y].piece:
                    moves.append((x+2, y))
        
        # BLACK
        # Forward
        if self.color == "black":
            if x > 1 and not board[x-1][y].piece:
                moves.append((x-1, y))
            # First move
            if not self.already_moved:
                if not board[x-1][y].piece and not board[x-2][y].piece:
                    moves.append((x-2, y))

        # WHITE
        # Takes
        if self.color == "white":
            if y == 0:
                if x < 8 and board[x+1][y+1].piece:
                    if board[x+1][y+1].piece.color == "black":
                        moves.append((x+1, y+1))
            elif y == 7:
                if x < 8 and board[x+1][y-1].piece:
                    if board[x+1][y-1].piece.color == "black":
                        moves.append((x+1, y-1))
            else:
                if x < 8 and board[x+1][y+1].piece:
                    if board[x+1][y+1].piece.color == "black":
                        moves.append((x+1, y+1))
                if x < 8 and board[x+1][y-1].piece:
                    if board[x+1][y-1].piece.color == "black":
                        moves.append((x+1, y-1))
        
        # BLACK
        # Takes
        if self.color == "black":
            if y == 0:
                if x > 0 and board[x-1][y+1].piece:
                    if board[x-1][y+1].piece.color == "white":
                        moves.append((x-1, y+1))
            elif y == 7:
                if x > 0 and board[x-1][y-1].piece:
                    if board[x-1][y-1].piece.color == "white":
                        moves.append((x-1, y-1))
            else:
                if x > 0 and board[x-1][y+1].piece:
                    if board[x-1][y+1].piece.color == "white":
                        moves.append((x-1, y+1))
                if x > 0 and board[x-1][y-1].piece:
                    if board[x-1][y-1].piece.color == "white":
                        moves.append((x-1, y-1))

        # En passant
        if self.color == "white":
            if x == 4:
                if y - 1 >= 0 and board[x][y-1].piece and isinstance(board[x][y-1].piece, Pawn) and board[x][y-1].piece.color == "black":
                    moves.append((x+1, y-1))
                if y + 1 < 8 and board[x][y+1].piece and isinstance(board[x][y+1].piece, Pawn) and board[x][y+1].piece.color == "black":
                    moves.append((x+1, y+1))
        
        if self.color == "black":
            if x == 3:
                if y - 1 >= 0 and board[x][y-1].piece and isinstance(board[x][y-1].piece, Pawn) and board[x][y-1].piece.color == "white":
                    moves.append((x-1, y-1))
                if y + 1 < 8 and board[x][y+1].piece and isinstance(board[x][y+1].piece, Pawn) and board[x][y+1].piece.color == "white":
                    moves.append((x-1, y+1))
                    

        st.session_state.all_legal_moves.extend(moves)
        return moves
    
    def get_attack_squares(self, x, y):
        attack_squares = []
        direction = 1 if self.color == 'white' else -1  # Direction of movement

        # Add diagonal attack squares
        if 0 <= x + direction < 8:
            if y - 1 >= 0:  # Left diagonal
                attack_squares.append((x + direction, y - 1))
            if y + 1 < 8:   # Right diagonal
                attack_squares.append((x + direction, y + 1))

        return attack_squares
