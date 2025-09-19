'use client';

import { Player } from '@/types/game';

interface GameBoardProps {
  board: Player[][];
  onCellClick: (row: number, col: number) => void;
  disabled?: boolean;
  winningCells?: [number, number][];
}

export default function GameBoard({
  board,
  onCellClick,
  disabled = false,
  winningCells = []
}: GameBoardProps) {
  const isWinningCell = (row: number, col: number) => {
    return winningCells.some(([r, c]) => r === row && c === col);
  };

  const getCellClassName = (row: number, col: number, value: Player) => {
    const baseClasses = "w-20 h-20 border-2 border-gray-400 flex items-center justify-center text-3xl font-bold cursor-pointer transition-all duration-200 hover:bg-gray-100";

    const playerClasses = {
      'X': 'text-blue-600',
      'O': 'text-red-600',
      '': 'text-gray-400'
    };

    const winningClass = isWinningCell(row, col) ? 'bg-green-200 border-green-500' : '';
    const disabledClass = disabled ? 'cursor-not-allowed opacity-50' : '';

    return `${baseClasses} ${playerClasses[value]} ${winningClass} ${disabledClass}`;
  };

  const handleCellClick = (row: number, col: number) => {
    if (!disabled && board[row][col] === '') {
      onCellClick(row, col);
    }
  };

  return (
    <div className="grid grid-cols-3 gap-1 w-fit mx-auto bg-gray-600 p-2 rounded-lg">
      {board.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <button
            key={`${rowIndex}-${colIndex}`}
            className={getCellClassName(rowIndex, colIndex, cell)}
            onClick={() => handleCellClick(rowIndex, colIndex)}
            disabled={disabled || cell !== ''}
            aria-label={`Cell ${rowIndex + 1}, ${colIndex + 1}: ${cell || 'empty'}`}
          >
            {cell}
          </button>
        ))
      )}
    </div>
  );
}