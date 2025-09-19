import pytest
from core.ai_algorithms import AIAlgorithms
from core.game_engine import GameEngine
from models import Move

class TestAIAlgorithms:
    
    def setup_method(self):
        self.ai = AIAlgorithms()
        self.engine = GameEngine()
    
    def test_evaluate_position_ai_win(self):
        """Test position evaluation for AI win."""
        board = [["O", "O", "O"], ["", "", ""], ["", "", ""]]
        score = self.ai.evaluate_position(board)
        assert score > 90  # Should be close to 100
    
    def test_evaluate_position_player_win(self):
        """Test position evaluation for player win."""
        board = [["X", "X", "X"], ["", "", ""], ["", "", ""]]
        score = self.ai.evaluate_position(board)
        assert score < -90  # Should be close to -100
    
    def test_evaluate_position_draw(self):
        """Test position evaluation for draw."""
        board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
        score = self.ai.evaluate_position(board)
        assert score == 0
    
    def test_minimax_winning_move(self):
        """Test minimax finds winning move."""
        # AI can win in one move
        board = [["O", "O", ""], ["X", "X", ""], ["", "", ""]]
        move, score = self.ai.minimax(board, 0, True, 9)
        
        assert move is not None
        assert move.row == 0 and move.col == 2  # Winning move
        assert score > 90
    
    def test_minimax_blocking_move(self):
        """Test minimax blocks opponent's winning move."""
        # Player can win in one move, AI should block
        board = [["X", "X", ""], ["O", "", ""], ["", "", ""]]
        move, score = self.ai.minimax(board, 0, True, 9)
        
        assert move is not None
        assert move.row == 0 and move.col == 2  # Blocking move
    
    def test_alpha_beta_same_as_minimax(self):
        """Test alpha-beta gives same result as minimax."""
        board = [["X", "", ""], ["", "O", ""], ["", "", ""]]
        
        minimax_move, minimax_score = self.ai.minimax(board, 0, True, 6)
        
        # Reset stats for alpha-beta
        self.ai._reset_stats()
        ab_move, ab_score = self.ai.alpha_beta(board, 0, float('-inf'), float('inf'), True, 6)
        
        # Should get same evaluation (moves might differ if multiple optimal moves exist)
        assert abs(minimax_score - ab_score) < 0.1
    
    def test_alpha_beta_pruning(self):
        """Test alpha-beta pruning reduces node exploration."""
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        
        # Run minimax
        self.ai._reset_stats()
        self.ai.minimax(board, 0, True, 4)
        minimax_nodes = self.ai.nodes_explored
        
        # Run alpha-beta
        self.ai._reset_stats()
        self.ai.alpha_beta(board, 0, float('-inf'), float('inf'), True, 4)
        ab_nodes = self.ai.nodes_explored
        
        # Alpha-beta should explore fewer or equal nodes
        assert ab_nodes <= minimax_nodes
        assert self.ai.pruned_branches >= 0
    
    def test_depth_limited_search(self):
        """Test depth-limited search respects depth limit."""
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        
        self.ai._reset_stats()
        move, score = self.ai.depth_limited_minimax(board, 3)
        
        assert move is not None
        assert self.ai.max_depth_reached <= 3
    
    def test_get_best_move_minimax(self):
        """Test get_best_move with minimax algorithm."""
        board = [["X", "", ""], ["", "O", ""], ["", "", ""]]
        
        move, analysis = self.ai.get_best_move(board, "minimax", "medium")
        
        assert isinstance(move, Move)
        assert 0 <= move.row <= 2
        assert 0 <= move.col <= 2
        assert analysis.nodes_explored > 0
        assert analysis.thinking_time >= 0
        assert "minimax" in analysis.move_reasoning.lower()
    
    def test_get_best_move_alpha_beta(self):
        """Test get_best_move with alpha-beta algorithm."""
        board = [["X", "", ""], ["", "O", ""], ["", "", ""]]
        
        move, analysis = self.ai.get_best_move(board, "alpha_beta", "hard")
        
        assert isinstance(move, Move)
        assert analysis.pruned_branches >= 0
        assert "alpha-beta" in analysis.move_reasoning.lower()
    
    def test_get_best_move_depth_limited(self):
        """Test get_best_move with depth-limited algorithm."""
        board = [["X", "", ""], ["", "O", ""], ["", "", ""]]
        
        move, analysis = self.ai.get_best_move(board, "depth_limited", "easy")
        
        assert isinstance(move, Move)
        assert analysis.max_depth_reached <= 3  # Easy difficulty
        assert "depth" in analysis.move_reasoning.lower()
    
    def test_difficulty_levels(self):
        """Test different difficulty levels affect search depth."""
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        
        # Easy difficulty
        move_easy, analysis_easy = self.ai.get_best_move(board, "minimax", "easy")
        
        # Hard difficulty  
        move_hard, analysis_hard = self.ai.get_best_move(board, "minimax", "hard")
        
        # Hard should explore more nodes (deeper search)
        assert analysis_hard.max_depth_reached >= analysis_easy.max_depth_reached
    
    def test_no_moves_available(self):
        """Test error when no moves are available."""
        board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
        
        with pytest.raises(ValueError, match="No available moves"):
            self.ai.get_best_move(board, "minimax", "medium")
    
    def test_single_move_available(self):
        """Test behavior when only one move is available."""
        board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", ""]]
        
        move, analysis = self.ai.get_best_move(board, "minimax", "medium")
        
        assert move.row == 2 and move.col == 2
        assert "only one move" in analysis.move_reasoning.lower()
    
    def test_ai_never_loses_optimal_play(self):
        """Test AI never loses when playing optimally from start."""
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        
        # AI goes first (should never lose)
        current_board = [row[:] for row in board]
        game_engine = GameEngine()
        
        moves_made = 0
        while not game_engine.is_game_over(current_board) and moves_made < 9:
            if moves_made % 2 == 0:  # AI turn
                move, _ = self.ai.get_best_move(current_board, "minimax", "hard")
                current_board = game_engine.make_move(current_board, move, "O")
            else:  # Simulate optimal human play (also use minimax but for X)
                # For testing, we'll make a simple move instead of full minimax
                available = game_engine.get_available_moves(current_board)
                if available:
                    current_board = game_engine.make_move(current_board, available[0], "X")
            
            moves_made += 1
        
        winner = game_engine.check_winner(current_board)
        # AI should win or draw, never lose
        assert winner != "X"