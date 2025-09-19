from fastapi import APIRouter, HTTPException
from typing import List
from models import AIRequest, AIResponse, AlgorithmInfo, ErrorResponse

router = APIRouter()

@router.post("/move", response_model=AIResponse)
async def get_ai_move(request: AIRequest):
    """
    Get AI move for the current game state using specified algorithm.
    """
    try:
        from core.game_engine import GameEngine
        from core.ai_algorithms import AIAlgorithms
        
        game_engine = GameEngine()
        ai_algorithms = AIAlgorithms()
        
        # Validate the game state
        if not game_engine.is_valid_board(request.board):
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse.create(
                    "INVALID_BOARD",
                    "Invalid board state provided"
                ).dict()
            )
        
        # Check if game is already over
        if game_engine.is_game_over(request.board):
            winner = game_engine.check_winner(request.board)
            if winner is None and game_engine.is_draw(request.board):
                winner = "draw"
            
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse.create(
                    "GAME_OVER",
                    f"Game is already over. Winner: {winner}"
                ).dict()
            )
        
        # Get AI move using specified algorithm
        try:
            best_move, analysis = ai_algorithms.get_best_move(
                board=request.board,
                algorithm=request.algorithm.value,
                difficulty=request.difficulty.value,
                max_depth=request.max_depth
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse.create(
                    "NO_MOVES_AVAILABLE",
                    str(e)
                ).dict()
            )
        
        # Make the AI move to check game state after move
        new_board = game_engine.make_move(request.board, best_move, "O")
        game_over = game_engine.is_game_over(new_board)
        winner = None
        
        if game_over:
            winner = game_engine.check_winner(new_board)
            if winner is None and game_engine.is_draw(new_board):
                winner = "draw"
        
        return AIResponse(
            move=best_move,
            evaluation=analysis.evaluation_score,
            analysis=analysis,
            game_over=game_over,
            winner=winner
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse.create(
                "INTERNAL_ERROR",
                str(e)
            ).dict()
        )

@router.get("/algorithms", response_model=List[AlgorithmInfo])
async def get_algorithms():
    """
    Get information about available AI algorithms.
    """
    return [
        AlgorithmInfo(
            name="minimax",
            description="Classic minimax algorithm with full game tree exploration",
            complexity="O(b^d)",
            best_for="Learning fundamentals and guaranteed optimal play"
        ),
        AlgorithmInfo(
            name="alpha_beta",
            description="Optimized minimax with alpha-beta pruning",
            complexity="O(b^(d/2)) best case",
            best_for="Faster optimal play with pruning demonstration"
        ),
        AlgorithmInfo(
            name="depth_limited",
            description="Minimax with configurable depth limits",
            complexity="O(b^d) where d is limited",
            best_for="Performance control and difficulty adjustment"
        )
    ]

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "tic-tac-toe-ai-backend"}