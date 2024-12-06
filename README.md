# Chess Game Review Engine

## Features

- Analyze chess positions using Stockfish
- Generate comprehensive game reports(coming soon)
- API-enabled for easy integration
- Supports FEN (Forsyth-Edwards Notation) analysis

## Quick Setup

1. **Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   .\venv\Scripts\activate   # On Windows
   pip install -r requirements.txt
   ```

2. **Download Stockfish:**
   - Download from [Stockfish website](https://stockfishchess.org/download/)
   - Place `stockfish.exe` in the project root

## API Usage

The Chess Game Review Engine provides a flexible API for chess position analysis Do a post request with a pgn:

`
localhost:5000/review_game
`

## Key Components

- Position analysis with detailed evaluations
- Move recommendations
- Game summary generation
- Flexible integration options

## Contributions

- Improve performance
- Add features
- Submit bug reports

## License

MIT License - see [LICENSE](LICENSE) file for details.