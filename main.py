import streamlit as st

from board import BoardCell, Board
from pieces import *

# TODO: En passant capture (movement is done)
# TODO: Castling
# TODO: Pawn promotion
# TODO: Reverse board view (black at the bottom (at the top of the screen))

if "game" not in st.session_state:
    print("NOVÁ HRA")
    st.session_state.game = Board()

if "whites_turn" not in st.session_state:
    st.session_state.whites_turn = True

if "active_piece" not in st.session_state:
    st.session_state.active_piece = None

if "legal_moves" not in st.session_state:
    st.session_state.legal_moves = []

if "all_legal_moves" not in st.session_state:
    st.session_state.all_legal_moves = []

if "pieces_can_move" not in st.session_state:
    st.session_state.pieces_can_move = []

#game.board.reverse()
print("RENDER")
st.session_state.game.render()

# Handle game result
if st.session_state.white_king_in_check and not st.session_state.pieces_can_move:
    st.warning("Checkmate! Black wins!")
elif st.session_state.black_king_in_check and not st.session_state.pieces_can_move:
    st.warning("Checkmate! White wins!")
elif not st.session_state.pieces_can_move:
    st.warning("Stalemate!")