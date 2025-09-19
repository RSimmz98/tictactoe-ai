from typing import List, Optional, Tuple
from models import GameState, Move, Player

class GameEngine:
    """
    Core game engine for tic-tac-toe logic and state management.
    """
    
    def __init__(self):
        self.winning_combinations = [
            # Rows
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # Columns
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # Diagonals
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]
    
    def is_valid_board(self, board: List[List[str]]) -> bool:
        """
        Validate if the board state is valid.
        """
        if len(board) != 3:
            return False
        
        for row in board:
            if len(row) != 3:
                return False
            for cell in row:
                if cell not in ["X", "O", ""]:
                    return False
        
        # Check if move counts are valid (X should have at most one more move than O)
        x_count = sum(row.count("X") for row in board)
        o_count = sum(row.count("O") for row in board)
        
        if x_count < o_count or x_count > o_count + 1:
            return False
        
        return True
    
    def is_valid_move(self, board: List[List[str]], row: int, col: int) -> bool:
        """
        Check if a move is valid (cell is empty and within bounds).
        """
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return False
        return board[row][col] == ""
    
    def make_move(self, board: List[List[str]], move: Move, player: str) -> List[List[str]]:
        """
        Make a move on the board and return new board state.
        """
        new_board = [row[:] for row in board]  # Deep copy
        new_board[move.row][move.col] = player
        return new_board
    
    def check_winner(self, board: List[List[str]]) -> Optional[str]:
        """
        Check if there's a winner on the board.
        Returns 'X', 'O', or None.
        """
        for combination in self.winning_combinations:
            cells = [board[row][col] for row, col in combination]
            if cells[0] != "" and all(cell == cells[0] for cell in cells):
                return cells[0]
        return None
    
    def is_draw(self, board: List[List[str]]) -> bool:
        """
        Check if the game is a draw (board full with no winner).
        """
        if self.check_winner(board) is not None:
            return False
        
        # Check if board is full
        for row in board:
            if "" in row:
                return False
        return True
    
    def is_game_over(self, board: List[List[str]]) -> bool:
        """
        Check if the game is over (winner or draw).
        """
        return self.check_winner(board) is not None or self.is_draw(board)
    
    def get_available_moves(self, board: List[List[str]]) -> List[Move]:
        """
        Get all available moves on the board.
        """
        moves = []
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    moves.append(Move(row=row, col=col))
        return moves
    
    def get_game_state(self, board: List[List[str]]) -> GameState:
        """
        Create a GameState object from the current board.
        """
        winner = self.check_winner(board)
        if winner is None and self.is_draw(board):
            winner = "draw"
        
        # Count moves to determine current player
        x_count = sum(row.count("X") for row in board)
        o_count = sum(row.count("O") for row in board)
        current_player = Player.O if x_count > o_count else Player.X
        
        return GameState(
            board=board,
            current_player=current_player,
            winner=winner,
            move_count=x_count + o_count
        )