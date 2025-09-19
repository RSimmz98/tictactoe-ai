import pytest
from core.game_engine import GameEngine
from models import Move

class TestGameEngine:
    
    def setup_method(self):
        self.engine = GameEngine()
    
    def test_is_valid_board_empty(self):
        """Test validation of empty board."""
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        assert self.engine.is_valid_board(board) == True
    
    def test_is_valid_board_invalid_size(self):
        """Test validation fails for wrong board size."""
        board = [["", ""], ["", ""]]
        assert self.engine.is_valid_board(board) == False
    
    def test_is_valid_board_invalid_characters(self):
        """Test validation fails for invalid characters."""
        board = [["X", "Y", ""], ["", "", ""], ["", "", ""]]
        assert self.engine.is_valid_board(board) == False
    
    def test_is_valid_board_invalid_move_count(self):
        """Test validation fails for invalid move counts."""
        # O has more moves than X
        board = [["O", "O", ""], ["", "", ""], ["", "", ""]]
        assert self.engine.is_valid_board(board) == False
    
    def test_is_valid_move(self):
        """Test move validation."""
        board = [["X", "", ""], ["", "", ""], ["", "", ""]]
        assert self.engine.is_valid_move(board, 0, 1) == True
        assert self.engine.is_valid_move(board, 0, 0) == False  # Occupied
        assert self.engine.is_valid_move(board, 3, 0) == False  # Out of bounds
    
    def test_make_move(self):
        """Test making a move."""
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        move = Move(row=1, col=1)
        new_board = self.engine.make_move(board, move, "X")
        
        assert new_board[1][1] == "X"
        assert board[1][1] == ""  # Original board unchanged
    
    def test_check_winner_row(self):
        """Test winner detection for rows."""
        board = [["X", "X", "X"], ["", "", ""], ["", "", ""]]
        assert self.engine.check_winner(board) == "X"
    
    def test_check_winner_column(self):
        """Test winner detection for columns."""
        board = [["O", "", ""], ["O", "", ""], ["O", "", ""]]
        assert self.engine.check_winner(board) == "O"
    
    def test_check_winner_diagonal(self):
        """Test winner detection for diagonals."""
        board = [["X", "", ""], ["", "X", ""], ["", "", "X"]]
        assert self.engine.check_winner(board) == "X"
    
    def test_check_winner_none(self):
        """Test no winner detection."""
        board = [["X", "O", ""], ["", "", ""], ["", "", ""]]
        assert self.engine.check_winner(board) == None
    
    def test_is_draw(self):
        """Test draw detection."""
        board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
        assert self.engine.is_draw(board) == True
    
    def test_is_not_draw_with_winner(self):
        """Test draw detection fails when there's a winner."""
        board = [["X", "X", "X"], ["O", "O", ""], ["", "", ""]]
        assert self.engine.is_draw(board) == False
    
    def test_get_available_moves(self):
        """Test getting available moves."""
        board = [["X", "", ""], ["", "O", ""], ["", "", ""]]
        moves = self.engine.get_available_moves(board)
        
        expected_positions = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        actual_positions = [(move.row, move.col) for move in moves]
        
        assert len(moves) == 7
        assert set(actual_positions) == set(expected_positions)
    
    def test_get_game_state(self):
        """Test game state creation."""
        board = [["X", "", ""], ["", "", ""], ["", "", ""]]
        game_state = self.engine.get_game_state(board)
        
        assert game_state.board == board
        assert game_state.current_player == "O"  # X just moved, O's turn
        assert game_state.winner == None
        assert game_state.move_count == 1