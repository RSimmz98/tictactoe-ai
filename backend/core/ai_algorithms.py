import time
import random
from typing import Tuple, Optional, Dict, Any
from models import Move, GameState, AlgorithmAnalysis
from core.game_engine import GameEngine

class AIAlgorithms:
    """
    Implementation of various AI search algorithms for tic-tac-toe.
    
    This class provides three main algorithms:
    1. Minimax - Classic game tree search
    2. Alpha-Beta Pruning - Optimized minimax with branch pruning
    3. Depth-Limited Search - Minimax with configurable depth limits
    """
    
    # Constants for better readability
    AI_PLAYER = "O"
    HUMAN_PLAYER = "X"
    WIN_SCORE = 100
    LOSE_SCORE = -100
    DRAW_SCORE = 0
    
    def __init__(self):
        self.game_engine = GameEngine()
        self._reset_stats()
    
    def _reset_stats(self):
        """Reset algorithm statistics for a new search."""
        self.nodes_explored = 0
        self.pruned_branches = 0
        self.max_depth_reached = 0
        self.start_time = time.time()
    
    def _create_analysis(self, move_reasoning: str, evaluation_score: float) -> AlgorithmAnalysis:
        """Create algorithm analysis with current statistics."""
        return AlgorithmAnalysis(
            nodes_explored=self.nodes_explored,
            pruned_branches=self.pruned_branches,
            max_depth_reached=self.max_depth_reached,
            thinking_time=time.time() - self.start_time,
            move_reasoning=move_reasoning,
            evaluation_score=evaluation_score
        )
    
    def evaluate_position(self, board: list, depth: int = 0) -> float:
        """
        Evaluate how good the current board position is.
        
        Returns:
            +100 to +90: AI wins (prefer quicker wins)
            -100 to -90: Human wins (delay losses)
            0: Draw or neutral position
            -10 to +10: Ongoing game with positional advantages
        """
        winner = self.game_engine.check_winner(board)
        
        # Terminal positions (game over)
        if winner == self.AI_PLAYER:
            return self.WIN_SCORE - depth  # Prefer quicker wins
        elif winner == self.HUMAN_PLAYER:
            return self.LOSE_SCORE + depth  # Delay losses if unavoidable
        elif self.game_engine.is_draw(board):
            return self.DRAW_SCORE
        
        # Non-terminal positions: use heuristic evaluation
        return self._calculate_position_value(board)
    
    def _calculate_position_value(self, board: list) -> float:
        """
        Calculate positional value for non-terminal positions.
        
        Strategy:
        - Center control is valuable (3 points)
        - Corner control is good (2 points each)
        - Edge positions are neutral
        """
        score = 0
        
        # Center square bonus (most valuable position)
        center_player = board[1][1]
        if center_player == self.AI_PLAYER:
            score += 3
        elif center_player == self.HUMAN_PLAYER:
            score -= 3
        
        # Corner squares bonus
        corner_positions = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for row, col in corner_positions:
            corner_player = board[row][col]
            if corner_player == self.AI_PLAYER:
                score += 2
            elif corner_player == self.HUMAN_PLAYER:
                score -= 2
        
        return score
    
    def minimax(self, board: list, depth: int, is_ai_turn: bool, max_depth: int = 9) -> Tuple[Optional[Move], float]:
        """
        Classic minimax algorithm - explores all possible game outcomes.
        
        How it works:
        1. If game is over or max depth reached, evaluate the position
        2. If AI's turn, try all moves and pick the one with highest score
        3. If human's turn, try all moves and pick the one with lowest score
        4. Recursively evaluate each possible move
        
        Args:
            board: Current game board
            depth: How deep we are in the search tree
            is_ai_turn: True if it's AI's turn, False if human's turn
            max_depth: Maximum depth to search
            
        Returns:
            (best_move, score) - The best move and its evaluation score
        """
        # Update search statistics
        self.nodes_explored += 1
        self.max_depth_reached = max(self.max_depth_reached, depth)
        
        # Base case: game over or reached maximum search depth
        if self._should_stop_search(board, depth, max_depth):
            return None, self.evaluate_position(board, depth)
        
        # Get all possible moves
        available_moves = self.game_engine.get_available_moves(board)
        
        if is_ai_turn:
            return self._maximize_score(board, depth, available_moves, max_depth)
        else:
            return self._minimize_score(board, depth, available_moves, max_depth)
    
    def _should_stop_search(self, board: list, depth: int, max_depth: int) -> bool:
        """Check if we should stop searching (terminal node or max depth)."""
        return self.game_engine.is_game_over(board) or depth >= max_depth
    
    def _maximize_score(self, board: list, depth: int, moves: list, max_depth: int) -> Tuple[Move, float]:
        """AI's turn: find the move that maximizes the score."""
        best_score = float('-inf')
        best_move = None
        
        for move in moves:
            # Try this move for AI
            new_board = self.game_engine.make_move(board, move, self.AI_PLAYER)
            
            # See what happens if human plays optimally after this move
            result = self.minimax(new_board, depth + 1, False, max_depth)
            move_from_recursion = result[0]  # We don't need this
            score = result[1]  # This is what we care about
            
            # Keep track of the best move so far
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move, best_score
    
    def _minimize_score(self, board: list, depth: int, moves: list, max_depth: int) -> Tuple[Move, float]:
        """Human's turn: find the move that minimizes the score (best for human)."""
        best_score = float('inf')
        best_move = None
        
        for move in moves:
            # Try this move for human
            new_board = self.game_engine.make_move(board, move, self.HUMAN_PLAYER)
            
            # See what happens if AI plays optimally after this move
            result = self.minimax(new_board, depth + 1, True, max_depth)
            move_from_recursion = result[0]  # We don't need this
            score = result[1]  # This is what we care about
            
            # Keep track of the best move for human (lowest score)
            if score < best_score:
                best_score = score
                best_move = move
        
        return best_move, best_score
    
    def alpha_beta(self, board: list, depth: int, alpha: float, beta: float, 
                   is_ai_turn: bool, max_depth: int = 9) -> Tuple[Optional[Move], float]:
        """
        Minimax with alpha-beta pruning - same as minimax but faster.
        
        How pruning works:
        - Alpha: best score AI can guarantee so far
        - Beta: best score human can guarantee so far  
        - If alpha >= beta, we can stop searching (prune the branch)
        
        Args:
            board: Current game board
            depth: Current search depth
            alpha: Best score AI can guarantee
            beta: Best score human can guarantee
            is_ai_turn: True if AI's turn, False if human's turn
            max_depth: Maximum search depth
            
        Returns:
            (best_move, score) - The best move and its evaluation score
        """
        # Update search statistics
        self.nodes_explored += 1
        self.max_depth_reached = max(self.max_depth_reached, depth)
        
        # Base case: game over or reached maximum search depth
        if self._should_stop_search(board, depth, max_depth):
            return None, self.evaluate_position(board, depth)
        
        # Get all possible moves
        available_moves = self.game_engine.get_available_moves(board)
        
        if is_ai_turn:
            return self._maximize_with_pruning(board, depth, available_moves, alpha, beta, max_depth)
        else:
            return self._minimize_with_pruning(board, depth, available_moves, alpha, beta, max_depth)
    
    def _maximize_with_pruning(self, board: list, depth: int, moves: list, 
                              alpha: float, beta: float, max_depth: int) -> Tuple[Move, float]:
        """AI's turn with alpha-beta pruning."""
        best_score = float('-inf')
        best_move = None
        
        for move in moves:
            # Try this move for AI
            new_board = self.game_engine.make_move(board, move, self.AI_PLAYER)
            
            # See what happens if human plays optimally after this move
            result = self.alpha_beta(new_board, depth + 1, alpha, beta, False, max_depth)
            move_from_recursion = result[0]  # We don't need this
            score = result[1]  # This is what we care about
            
            # Keep track of the best move so far
            if score > best_score:
                best_score = score
                best_move = move
            
            # Update alpha (best score AI can guarantee)
            alpha = max(alpha, score)
            
            # Pruning: if AI can guarantee better than what human allows, stop searching
            if beta <= alpha:
                self.pruned_branches += 1
                break  # Beta cutoff - no need to check remaining moves
        
        return best_move, best_score
    
    def _minimize_with_pruning(self, board: list, depth: int, moves: list,
                              alpha: float, beta: float, max_depth: int) -> Tuple[Move, float]:
        """Human's turn with alpha-beta pruning."""
        best_score = float('inf')
        best_move = None
        
        for move in moves:
            # Try this move for human
            new_board = self.game_engine.make_move(board, move, self.HUMAN_PLAYER)
            
            # See what happens if AI plays optimally after this move
            result = self.alpha_beta(new_board, depth + 1, alpha, beta, True, max_depth)
            move_from_recursion = result[0]  # We don't need this
            score = result[1]  # This is what we care about
            
            # Keep track of the best move for human (lowest score)
            if score < best_score:
                best_score = score
                best_move = move
            
            # Update beta (best score human can guarantee)
            beta = min(beta, score)
            
            # Pruning: if human can guarantee better than what AI allows, stop searching
            if beta <= alpha:
                self.pruned_branches += 1
                break  # Alpha cutoff - no need to check remaining moves
        
        return best_move, best_score
    
    def depth_limited_minimax(self, board: list, max_depth: int) -> Tuple[Optional[Move], float]:
        """
        Depth-limited minimax search - minimax but only search to a certain depth.
        
        This is useful for:
        - Controlling difficulty (shallow search = easier AI)
        - Managing computation time
        - Testing different search depths
        
        Args:
            board: Current game board
            max_depth: How deep to search (1 = only look at immediate moves)
            
        Returns:
            (best_move, score) - The best move and its evaluation score
        """
        return self.minimax(board, 0, True, max_depth)
    
    def get_best_move(self, board: list, algorithm: str = "minimax", 
                     difficulty: str = "medium", max_depth: Optional[int] = None) -> Tuple[Move, AlgorithmAnalysis]:
        """
        Get the best move using the specified algorithm and difficulty.
        
        This is the main entry point for getting AI moves.
        
        Args:
            board: Current game board
            algorithm: Which algorithm to use ('minimax', 'alpha_beta', 'depth_limited')
            difficulty: How hard the AI should play ('easy', 'medium', 'hard')
            max_depth: Override search depth (if None, uses difficulty setting)
            
        Returns:
            (best_move, analysis) - The chosen move and detailed analysis
        """
        self._reset_stats()
        
        # Determine search depth based on difficulty
        search_depth = self._get_search_depth(difficulty, max_depth)
        
        # Get all possible moves
        available_moves = self.game_engine.get_available_moves(board)
        
        # Handle edge cases
        if not available_moves:
            raise ValueError("No available moves on the board")
        
        if len(available_moves) == 1:
            # Only one move possible - no need to search
            move = available_moves[0]
            analysis = self._create_analysis("Only one move available", 0.0)
            return move, analysis
        
        # Run the chosen algorithm
        best_move, eval_score, move_reasoning = self._run_algorithm(
            board, algorithm, search_depth
        )
        
        # Handle algorithm failure
        if best_move is None:
            best_move = available_moves[0]
            eval_score = 0.0
            move_reasoning = "Fallback to first available move"
        
        # Apply difficulty adjustments
        final_move = self._apply_difficulty_adjustments(
            best_move, available_moves, difficulty, move_reasoning
        )
        
        # Create final analysis
        analysis = self._create_analysis(move_reasoning, eval_score)
        return final_move, analysis
    
    def _get_search_depth(self, difficulty: str, max_depth: Optional[int]) -> int:
        """Determine how deep to search based on difficulty."""
        if max_depth is not None:
            return max_depth
        
        depth_settings = {
            "easy": 3,    # Look ahead 3 moves
            "medium": 6,  # Look ahead 6 moves  
            "hard": 9     # Search to end of game
        }
        return depth_settings.get(difficulty, 6)
    
    def _run_algorithm(self, board: list, algorithm: str, search_depth: int) -> Tuple[Optional[Move], float, str]:
        """Run the specified algorithm and return results."""
        if algorithm == "alpha_beta":
            result = self.alpha_beta(board, 0, float('-inf'), float('inf'), True, search_depth)
            best_move = result[0]
            eval_score = result[1]
            reasoning = f"Alpha-beta pruning found best move (pruned {self.pruned_branches} branches)"
            
        elif algorithm == "depth_limited":
            result = self.depth_limited_minimax(board, search_depth)
            best_move = result[0]
            eval_score = result[1]
            reasoning = f"Depth-limited search to depth {search_depth}"
            
        else:  # minimax
            result = self.minimax(board, 0, True, search_depth)
            best_move = result[0]
            eval_score = result[1]
            reasoning = "Classic minimax algorithm"
        
        return best_move, eval_score, reasoning
    
    def _apply_difficulty_adjustments(self, best_move: Move, available_moves: list, 
                                    difficulty: str, move_reasoning: str) -> Move:
        """Apply difficulty-based adjustments to the chosen move."""
        if difficulty == "easy" and len(available_moves) > 1:
            # 30% chance of making a random move instead of optimal move
            if random.random() < 0.3:
                random_move = random.choice(available_moves)
                move_reasoning = "Random move for easy difficulty"
                return random_move
        
        return best_move