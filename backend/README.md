# Tic-Tac-Toe AI Backend

Python FastAPI backend implementing various AI search algorithms for tic-tac-toe.

## Features

- **Multiple AI Algorithms**: Minimax, Alpha-Beta Pruning, Depth-Limited Search
- **Educational Focus**: Algorithm analysis and visualization data
- **RESTful API**: Clean API interface for frontend integration
- **Comprehensive Testing**: Unit tests for all core functionality

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

- `POST /api/move` - Get AI move for current game state
- `GET /api/algorithms` - Get information about available algorithms
- `GET /api/health` - Health check endpoint

## Testing

Run tests with:
```bash
pytest
```

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── models/             # Pydantic data models
├── api/                # API routes and endpoints
├── core/               # Core game logic and AI algorithms
└── tests/              # Unit tests
```