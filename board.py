from pieces import Pawn, Rook, Knight, Bishop, Queen, King
import streamlit as st

class Board:
    def __init__(self):
        self.board = self.create_board()
    
    def create_board(self):
        grid = []
        for x in range(8):
            rank = []
            for y in range(8):
                piece = self.get_piece(x, y)
                cell = BoardCell(x, y, piece)
                rank.append(cell)
            grid.append(rank)
        return grid
    
    def get_piece(self, x, y):
        if x in [0, 1]: color = "white"
        elif x in [6, 7]: color = "black"

        if x in [1, 6]: return Pawn(color, y)
        elif x in [0, 7]:
            if y == 0 or y == 7: return Rook(color, y)
            if y == 1 or y == 6: return Knight(color, y)
            if y == 2 or y == 5: return Bishop(color, y)
            if y == 3: return Queen(color, y)
            if y == 4: return King(color)

    def render(self):
        streamlit_columns = st.columns(8)
        for rank in self.board:
            for cell in rank:
                with streamlit_columns[cell.y]:
                    cell.render(self)
    
    def is_king_in_check(self, color):
        # Get king position
        king_position = self.find_king_position(color)
        
        # Check if any piece of opposite color can attack the king
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if piece and piece.color != color:
                    if king_position in piece.get_moves(self.board, i, j):
                        st.session_state[f"{color}_king_in_check"] = True
                        return True
        st.session_state[f"{color}_king_in_check"] = False
        return False

    def find_king_position(self, color):
        # Find king position
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if isinstance(piece, King) and piece.color == color:
                    return (i, j)
        return None

    def is_move_legal_in_check(self, start_pos, end_pos, color):
        # Position backup
        piece_backup = self.board[end_pos[0]][end_pos[1]].piece
        moving_piece = self.board[start_pos[0]][start_pos[1]].piece

        # Simulate move
        self.board[end_pos[0]][end_pos[1]].piece = moving_piece
        self.board[start_pos[0]][start_pos[1]].piece = None

        # Check if king is in check after move
        in_check_after_move = self.is_king_in_check(color)

        # Revert move
        self.board[start_pos[0]][start_pos[1]].piece = moving_piece
        self.board[end_pos[0]][end_pos[1]].piece = piece_backup

        # Return if king is not in check after move
        return not in_check_after_move

class BoardCell:
    def __init__(self, x, y, piece = None):
        """
        x = rank
        y = file
        """
        self.x = x
        self.y = y
        self.piece = piece
        self.key = f"{x}_{y}"
        self.disabled = True
        self.help = None

    def has_legal_moves(self, board):
        if self.piece: return self.piece.get_moves(board, self.x, self.y)
        else: return False

    def render(self, board):
            # Is cell active?
            is_active = (self.x, self.y) == st.session_state.get('active_piece', (None, None))
            is_any_active = st.session_state.get('active_piece') is not None

            # Has cell legal moves?
            is_legal_move = (self.x, self.y) in st.session_state.get('legal_moves', [])

            # Is it white's turn?
            is_whites_turn = st.session_state.get('whites_turn')

            # Is king in check?
            is_king_in_check = board.is_king_in_check(self.piece.color if self.piece else None)

            # Enable button if cell has legal moves and there is no any other active cell, or if this cell is active
            if is_king_in_check and self.piece and ((self.piece.color == "white" and is_whites_turn) or (self.piece.color == "black" and not is_whites_turn)):
                legal_moves_in_check = [move for move in self.piece.get_moves(board.board, self.x, self.y) if board.is_move_legal_in_check((self.x, self.y), move, self.piece.color)]
                is_disabled = not legal_moves_in_check
                if not is_disabled: st.session_state.pieces_can_move.append((self.x, self.y))
                return st.button(self.piece.icon, key=self.key, disabled=is_disabled, help=self.help, on_click=self.handle_click, args=(self.x, self.y, board, legal_moves_in_check))

            if is_legal_move:
                # If cell has legal moves, enable button
                try: return st.button(self.piece.icon, key=self.key, disabled=False, help=self.help, on_click=self.move_piece, args=(self.x, self.y, board))
                except: return st.button("‎ ‎ ‎ ‎ ‎ ‎", key=self.key, disabled=False, help=self.help, on_click=self.move_piece, args=(self.x, self.y, board))
            elif self.piece and ((self.piece.color == "white" and is_whites_turn) or (self.piece.color == "black" and not is_whites_turn)):
                has_legal_moves = self.has_legal_moves(st.session_state.game.board)
                is_disabled = not (has_legal_moves and not is_any_active) and not is_active
                if not is_disabled: st.session_state.pieces_can_move.append((self.x, self.y))
                return st.button(self.piece.icon, key=self.key, disabled=is_disabled, help=self.help, on_click=self.handle_click, args=(self.x, self.y, board))
            elif self.piece:
                return st.button(self.piece.icon, key=self.key, disabled=True, help=self.help, on_click=self.handle_click, args=(self.x, self.y, board))
            else:
                # Disable empty cell
                return st.button("‎ ‎ ‎ ‎ ‎ ‎", key=self.key, disabled=True)

    @staticmethod  
    def handle_click(x, y, board: Board, legal_moves = []):
        print(f"Clicked on {x}, {y}")
        
        # Update piece state
        current_active = st.session_state.get('active_piece')
        if current_active == (x, y):
            # If clicked on the same cell, reset active piece
            st.session_state.active_piece = None
            st.session_state.legal_moves = []
        else:
            st.session_state.active_piece = (x, y)
            piece_moves = board.board[x][y].piece.get_moves(board.board, x, y)
            if legal_moves: piece_moves = [move for move in piece_moves if move in legal_moves] # Filter illegal moves if king is in check
            st.session_state.legal_moves = piece_moves

    @staticmethod
    def move_piece(x, y, board: Board):
        print(f"Moving to {x}, {y}")

        # Move piece to x, y
        piece = board.board[st.session_state.get('active_piece')[0]][st.session_state.get('active_piece')[1]].piece
        board.board[x][y].piece = piece
        if isinstance(piece, Pawn): piece.already_moved = True

        # Remove piece from original position
        board.board[st.session_state.get('active_piece')[0]][st.session_state.get('active_piece')[1]].piece = None

        # Clear active piece and legal moves, change turn
        st.session_state.active_piece = None
        st.session_state.legal_moves = []
        st.session_state.whites_turn = not st.session_state.whites_turn
        st.session_state.all_legal_moves = []
        st.session_state.pieces_can_move = []

        

