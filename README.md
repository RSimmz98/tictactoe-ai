# Tic-Tac-Toe AI Game

An educational tic-tac-toe game featuring multiple AI search algorithms with real-time visualization and analysis. Built with Next.js frontend and Python FastAPI backend.

## 🎯 Features

### AI Algorithms
- **Minimax Algorithm** - Classic game tree search with guaranteed optimal play
- **Alpha-Beta Pruning** - Optimized minimax with branch pruning for faster computation
- **Depth-Limited Search** - Configurable search depth for difficulty control

### Educational Features
- Real-time algorithm analysis and statistics
- Move reasoning explanations
- Performance comparisons between algorithms
- Visualization of AI decision-making process

### Game Features
- Interactive web-based tic-tac-toe board
- Multiple difficulty levels (Easy, Medium, Hard)
- Algorithm selection and configuration
- Game statistics and move history

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST API    ┌─────────────────┐
│   Next.js       │◄──────────────────►│   Python        │
│   Frontend      │                     │   Backend       │
│                 │                     │                 │
│ - Game UI       │                     │ - AI Algorithms │
│ - Visualization │                     │ - Game Logic    │
│ - Controls      │                     │ - Analysis      │
└─────────────────┘                     └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🧠 AI Algorithms Explained

### Minimax Algorithm
The classic game tree search algorithm that explores all possible game outcomes to find the optimal move.

**How it works:**
1. Generate all possible moves
2. For each move, recursively evaluate all possible opponent responses
3. Choose the move that maximizes AI's score while minimizing opponent's score
4. Guarantees optimal play but can be computationally expensive

**Time Complexity:** O(b^d) where b = branching factor, d = depth

### Alpha-Beta Pruning
An optimization of minimax that eliminates branches that cannot affect the final decision.

**How it works:**
1. Maintains alpha (best maximizer score) and beta (best minimizer score)
2. Prunes branches when beta ≤ alpha (no need to explore further)
3. Achieves same result as minimax but with fewer node evaluations
4. Can reduce time complexity significantly in practice

**Time Complexity:** O(b^(d/2)) in best case

### Depth-Limited Search
Minimax with a configurable maximum search depth for performance control.

**How it works:**
1. Limits search to a specified depth
2. Uses heuristic evaluation for non-terminal positions at depth limit
3. Allows for difficulty adjustment and performance tuning
4. Balances move quality with computation time

## 📁 Project Structure

```
tic-tac-toe-ai/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Server entry point
│   ├── api/                # API routes and endpoints
│   ├── core/               # Game logic and AI algorithms
│   ├── models/             # Data models and schemas
│   └── tests/              # Unit tests
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── lib/           # Utilities and API client
│   │   └── types/         # TypeScript type definitions
│   └── public/            # Static assets
├── .kiro/                 # Kiro IDE specifications
│   └── specs/             # Feature specifications and tasks
└── README.md              # This file
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Run specific test files:
```bash
pytest tests/test_ai_algorithms.py -v
pytest tests/test_game_engine.py -v
```

## 🎮 How to Play

1. Open the game in your browser at `http://localhost:3000`
2. Select your preferred AI algorithm and difficulty level
3. Click on any empty cell to make your move (you play as X)
4. The AI will automatically respond with its move (playing as O)
5. Continue until someone wins or the game ends in a draw

## 📊 Algorithm Analysis

The game provides detailed analysis of each AI move including:

- **Nodes Explored**: How many game positions the AI evaluated
- **Pruned Branches**: Number of branches eliminated (alpha-beta only)
- **Search Depth**: Maximum depth reached in the game tree
- **Thinking Time**: Time taken to calculate the move
- **Move Reasoning**: Explanation of why the AI chose this move
- **Evaluation Score**: Numerical assessment of the position

## 🎓 Educational Value

This project demonstrates key concepts in:

- **Game Theory**: Zero-sum games, optimal strategies
- **Search Algorithms**: Tree traversal, pruning techniques
- **Algorithm Analysis**: Time complexity, space complexity
- **Artificial Intelligence**: Decision making, evaluation functions
- **Software Architecture**: API design, separation of concerns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built as an educational tool for learning AI search algorithms
- Inspired by classic game theory and artificial intelligence concepts
- Developed using modern web technologies and best practices