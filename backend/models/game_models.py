from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class Player(str, Enum):
    X = "X"
    O = "O"
    EMPTY = ""

class Algorithm(str, Enum):
    MINIMAX = "minimax"
    ALPHA_BETA = "alpha_beta"
    DEPTH_LIMITED = "depth_limited"

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Move(BaseModel):
    row: int = Field(..., ge=0, le=2, description="Row index (0-2)")
    col: int = Field(..., ge=0, le=2, description="Column index (0-2)")
    score: Optional[float] = Field(None, description="Move evaluation score")

class GameState(BaseModel):
    board: List[List[str]] = Field(..., description="3x3 game board")
    current_player: Player = Field(default=Player.X, description="Current player")
    winner: Optional[str] = Field(None, description="Game winner or None")
    move_count: int = Field(default=0, description="Number of moves made")
    
    @field_validator('board')
    @classmethod
    def validate_board(cls, v):
        if len(v) != 3:
            raise ValueError('Board must have exactly 3 rows')
        for row in v:
            if len(row) != 3:
                raise ValueError('Each row must have exactly 3 columns')
            for cell in row:
                if cell not in ["X", "O", ""]:
                    raise ValueError('Board cells must be "X", "O", or empty string')
        return v

class AlgorithmAnalysis(BaseModel):
    nodes_explored: int = Field(default=0, description="Number of nodes explored")
    pruned_branches: int = Field(default=0, description="Number of pruned branches")
    max_depth_reached: int = Field(default=0, description="Maximum depth reached")
    thinking_time: float = Field(default=0.0, description="Time taken in seconds")
    move_reasoning: str = Field(default="", description="Explanation of move choice")
    evaluation_score: float = Field(default=0.0, description="Position evaluation score")
    game_tree: Optional[Dict[str, Any]] = Field(None, description="Game tree for visualization")

class AIRequest(BaseModel):
    board: List[List[str]] = Field(..., description="Current game board state")
    algorithm: Algorithm = Field(default=Algorithm.MINIMAX, description="AI algorithm to use")
    difficulty: Difficulty = Field(default=Difficulty.MEDIUM, description="Difficulty level")
    visualization: bool = Field(default=False, description="Include visualization data")
    max_depth: Optional[int] = Field(None, description="Maximum search depth")

class AIResponse(BaseModel):
    move: Move = Field(..., description="AI's chosen move")
    evaluation: float = Field(..., description="Position evaluation")
    analysis: AlgorithmAnalysis = Field(..., description="Algorithm analysis data")
    game_over: bool = Field(default=False, description="Whether game is over")
    winner: Optional[str] = Field(None, description="Winner if game is over")

class AlgorithmInfo(BaseModel):
    name: str = Field(..., description="Algorithm name")
    description: str = Field(..., description="Algorithm description")
    complexity: str = Field(..., description="Time complexity")
    best_for: str = Field(..., description="Best use case")

class ErrorResponse(BaseModel):
    error: Dict[str, Any] = Field(..., description="Error details")
    
    @classmethod
    def create(cls, code: str, message: str, details: Optional[Dict] = None):
        return cls(error={
            "code": code,
            "message": message,
            "details": details or {}
        })