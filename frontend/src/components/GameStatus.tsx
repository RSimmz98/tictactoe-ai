'use client';

import { Player } from '@/types/game';

interface GameStatusProps {
  currentPlayer: Player;
  winner: string | null;
  isAIThinking: boolean;
  moveCount: number;
}

export default function GameStatus({
  currentPlayer,
  winner,
  isAIThinking,
  moveCount
}: GameStatusProps) {
  const getStatusMessage = () => {
    if (winner) {
      if (winner === 'draw') {
        return "It's a draw! 🤝";
      }
      return winner === 'X' ? "You win! 🎉" : "AI wins! 🤖";
    }

    if (isAIThinking) {
      return "AI is thinking... 🤔";
    }

    return currentPlayer === 'X' ? "Your turn" : "AI's turn";
  };

  const getStatusColor = () => {
    if (winner) {
      if (winner === 'draw') return 'text-yellow-600';
      return winner === 'X' ? 'text-green-600' : 'text-red-600';
    }

    if (isAIThinking) return 'text-blue-600';
    return currentPlayer === 'X' ? 'text-blue-600' : 'text-purple-600';
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md text-center">
      <div className={`text-xl font-semibold ${getStatusColor()}`}>
        {getStatusMessage()}
      </div>
      
      {!winner && (
        <div className="text-sm text-gray-500 mt-2">
          Move {moveCount + 1} • {currentPlayer === 'X' ? 'You are X' : 'AI is O'}
        </div>
      )}

      {isAIThinking && (
        <div className="mt-2">
          <div className="inline-flex items-center space-x-1">
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
        </div>
      )}
    </div>
  );
}