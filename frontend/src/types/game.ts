export type Player = 'X' | 'O' | '';

export type Algorithm = 'minimax' | 'alpha_beta' | 'depth_limited';

export type Difficulty = 'easy' | 'medium' | 'hard';

export interface Move {
  row: number;
  col: number;
  score?: number;
}

export interface GameState {
  board: Player[][];
  currentPlayer: Player;
  winner: string | null;
  moveCount: number;
}

export interface AlgorithmAnalysis {
  nodes_explored: number;
  pruned_branches: number;
  max_depth_reached: number;
  thinking_time: number;
  move_reasoning: string;
  evaluation_score: number;
  game_tree?: any;
}

export interface AIRequest {
  board: Player[][];
  algorithm: Algorithm;
  difficulty: Difficulty;
  visualization: boolean;
  max_depth?: number;
}

export interface AIResponse {
  move: Move;
  evaluation: number;
  analysis: AlgorithmAnalysis;
  game_over: boolean;
  winner: string | null;
}

export interface AlgorithmInfo {
  name: string;
  description: string;
  complexity: string;
  best_for: string;
}

export interface GameConfig {
  algorithm: Algorithm;
  difficulty: Difficulty;
  visualization: boolean;
  maxDepth?: number;
}