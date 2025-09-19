'use client';

import { Algorithm, Difficulty, GameConfig } from '@/types/game';

interface GameControlsProps {
  config: GameConfig;
  onConfigChange: (config: GameConfig) => void;
  onNewGame: () => void;
  disabled?: boolean;
}

export default function GameControls({
  config,
  onConfigChange,
  onNewGame,
  disabled = false
}: GameControlsProps) {
  const handleAlgorithmChange = (algorithm: Algorithm) => {
    onConfigChange({ ...config, algorithm });
  };

  const handleDifficultyChange = (difficulty: Difficulty) => {
    onConfigChange({ ...config, difficulty });
  };

  const handleVisualizationToggle = () => {
    onConfigChange({ ...config, visualization: !config.visualization });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
      <h3 className="text-lg font-semibold text-gray-800">Game Settings</h3>
      
      {/* Algorithm Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          AI Algorithm
        </label>
        <select
          value={config.algorithm}
          onChange={(e) => handleAlgorithmChange(e.target.value as Algorithm)}
          disabled={disabled}
          className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
        >
          <option value="minimax">Minimax</option>
          <option value="alpha_beta">Alpha-Beta Pruning</option>
          <option value="depth_limited">Depth-Limited Search</option>
        </select>
      </div>

      {/* Difficulty Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Difficulty Level
        </label>
        <select
          value={config.difficulty}
          onChange={(e) => handleDifficultyChange(e.target.value as Difficulty)}
          disabled={disabled}
          className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      {/* Visualization Toggle */}
      <div className="flex items-center space-x-2">
        <input
          type="checkbox"
          id="visualization"
          checked={config.visualization}
          onChange={handleVisualizationToggle}
          disabled={disabled}
          className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 disabled:opacity-50"
        />
        <label htmlFor="visualization" className="text-sm font-medium text-gray-700">
          Show AI Analysis
        </label>
      </div>

      {/* New Game Button */}
      <button
        onClick={onNewGame}
        disabled={disabled}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        New Game
      </button>
    </div>
  );
}