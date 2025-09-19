'use client';

import { AlgorithmAnalysis } from '@/types/game';

interface AnalysisPanelProps {
  analysis: AlgorithmAnalysis | null;
  visible: boolean;
}

export default function AnalysisPanel({ analysis, visible }: AnalysisPanelProps) {
  if (!visible || !analysis) {
    return null;
  }

  const formatTime = (seconds: number) => {
    if (seconds < 0.001) return '< 1ms';
    if (seconds < 1) return `${Math.round(seconds * 1000)}ms`;
    return `${seconds.toFixed(2)}s`;
  };

  const formatScore = (score: number) => {
    if (score > 0) return `+${score.toFixed(2)}`;
    return score.toFixed(2);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">AI Analysis</h3>
      
      <div className="space-y-3">
        {/* Performance Metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-blue-50 p-3 rounded">
            <div className="text-sm text-blue-600 font-medium">Nodes Explored</div>
            <div className="text-xl font-bold text-blue-800">
              {analysis.nodes_explored.toLocaleString()}
            </div>
          </div>
          
          <div className="bg-green-50 p-3 rounded">
            <div className="text-sm text-green-600 font-medium">Thinking Time</div>
            <div className="text-xl font-bold text-green-800">
              {formatTime(analysis.thinking_time)}
            </div>
          </div>
        </div>

        {/* Algorithm-specific metrics */}
        {analysis.pruned_branches > 0 && (
          <div className="bg-purple-50 p-3 rounded">
            <div className="text-sm text-purple-600 font-medium">Branches Pruned</div>
            <div className="text-xl font-bold text-purple-800">
              {analysis.pruned_branches.toLocaleString()}
            </div>
            <div className="text-xs text-purple-600 mt-1">
              {((analysis.pruned_branches / (analysis.nodes_explored + analysis.pruned_branches)) * 100).toFixed(1)}% efficiency
            </div>
          </div>
        )}

        {/* Evaluation and Reasoning */}
        <div className="border-t pt-3">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Position Score</span>
            <span className={`font-bold ${analysis.evaluation_score >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {formatScore(analysis.evaluation_score)}
            </span>
          </div>
          
          {analysis.max_depth_reached > 0 && (
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">Max Depth</span>
              <span className="font-bold text-gray-800">{analysis.max_depth_reached}</span>
            </div>
          )}
        </div>

        {/* Move Reasoning */}
        {analysis.move_reasoning && (
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-sm font-medium text-gray-700 mb-1">AI Reasoning</div>
            <div className="text-sm text-gray-600 italic">
              "{analysis.move_reasoning}"
            </div>
          </div>
        )}
      </div>
    </div>
  );
}