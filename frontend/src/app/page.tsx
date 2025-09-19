'use client';

import { useState, useCallback } from 'react';
import GameBoard from '@/components/GameBoard';
import GameControls from '@/components/GameControls';
import GameStatus from '@/components/GameStatus';
import AnalysisPanel from '@/components/AnalysisPanel';
import { GameLogic } from '@/lib/gameLogic';
import { GameAPI } from '@/lib/api';
import { Player, GameConfig, AlgorithmAnalysis, Move } from '@/types/game';

export default function Home() {
  const [board, setBoard] = useState<Player[][]>(GameLogic.createEmptyBoard());
  const [currentPlayer, setCurrentPlayer] = useState<Player>('X');
  const [winner, setWinner] = useState<string | null>(null);
  const [isAIThinking, setIsAIThinking] = useState(false);
  const [analysis, setAnalysis] = useState<AlgorithmAnalysis | null>(null);
  const [config, setConfig] = useState<GameConfig>({
    algorithm: 'minimax',
    difficulty: 'medium',
    visualization: true
  });

  const checkGameEnd = useCallback((newBoard: Player[][]) => {
    const gameWinner = GameLogic.checkWinner(newBoard);
    if (gameWinner) {
      setWinner(gameWinner);
      return true;
    }
    return false;
  }, []);

  const makeAIMove = useCallback(async (gameBoard: Player[][]) => {
    if (isAIThinking) return;
    
    setIsAIThinking(true);
    setAnalysis(null);

    try {
      const response = await GameAPI.getAIMove({
        board: gameBoard,
        algorithm: config.algorithm,
        difficulty: config.difficulty,
        visualization: config.visualization
      });

      // Simulate thinking time for better UX
      await new Promise(resolve => setTimeout(resolve, 500));

      const newBoard = GameLogic.makeMove(gameBoard, response.move, 'O');
      setBoard(newBoard);
      setCurrentPlayer('X');
      
      if (config.visualization) {
        setAnalysis(response.analysis);
      }

      checkGameEnd(newBoard);
    } catch (error) {
      console.error('AI move failed:', error);
      // For now, make a random move as fallback
      const availableMoves = GameLogic.getAvailableMoves(gameBoard);
      if (availableMoves.length > 0) {
        const randomMove = availableMoves[Math.floor(Math.random() * availableMoves.length)];
        const newBoard = GameLogic.makeMove(gameBoard, randomMove, 'O');
        setBoard(newBoard);
        setCurrentPlayer('X');
        checkGameEnd(newBoard);
      }
    } finally {
      setIsAIThinking(false);
    }
  }, [config, isAIThinking, checkGameEnd]);

  const handleCellClick = useCallback(async (row: number, col: number) => {
    if (winner || isAIThinking || currentPlayer !== 'X') return;
    if (!GameLogic.isValidMove(board, row, col)) return;

    const move: Move = { row, col };
    const newBoard = GameLogic.makeMove(board, move, 'X');
    setBoard(newBoard);
    setCurrentPlayer('O');

    if (!checkGameEnd(newBoard)) {
      // AI's turn
      await makeAIMove(newBoard);
    }
  }, [board, currentPlayer, winner, isAIThinking, checkGameEnd, makeAIMove]);

  const handleNewGame = useCallback(() => {
    const emptyBoard = GameLogic.createEmptyBoard();
    setBoard(emptyBoard);
    setCurrentPlayer('X');
    setWinner(null);
    setIsAIThinking(false);
    setAnalysis(null);
  }, []);

  const handleConfigChange = useCallback((newConfig: GameConfig) => {
    setConfig(newConfig);
  }, []);

  const moveCount = GameLogic.getMoveCount(board);

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Tic-Tac-Toe AI
          </h1>
          <p className="text-gray-600">
            Play against AI with different search algorithms
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Game Controls */}
          <div className="lg:col-span-1">
            <GameControls
              config={config}
              onConfigChange={handleConfigChange}
              onNewGame={handleNewGame}
              disabled={isAIThinking}
            />
          </div>

          {/* Game Board and Status */}
          <div className="lg:col-span-1 space-y-6">
            <GameStatus
              currentPlayer={currentPlayer}
              winner={winner}
              isAIThinking={isAIThinking}
              moveCount={moveCount}
            />
            
            <GameBoard
              board={board}
              onCellClick={handleCellClick}
              disabled={winner !== null || isAIThinking || currentPlayer !== 'X'}
            />
          </div>

          {/* Analysis Panel */}
          <div className="lg:col-span-1">
            <AnalysisPanel
              analysis={analysis}
              visible={config.visualization}
            />
          </div>
        </div>
      </div>
    </div>
  );
}