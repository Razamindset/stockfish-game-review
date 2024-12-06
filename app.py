from flask import Flask, request, jsonify
from src.utils.parse_pgn import parse_pgn
from src.utils.analyze import analyze_position
from src.utils.generate_report import generate_report
from src.utils.stockfish_pool import StockfishPool
import os
import asyncio


app = Flask(__name__)

# Initialize the Stockfish pool
stockfish_pool = StockfishPool(
    pool_size=os.cpu_count() or 4  # Use number of CPU cores
)

@app.route('/review_game', methods=['POST'])
def review_game():
    pgn_data = request.json.get('pgn')
    

    if not pgn_data:
        return jsonify({"error": "No PGN data provided"}), 400

    try:
        # Step 1: Parse PGN
        fen_list = parse_pgn(pgn_data)

        analysis_results = []
        for fen in fen_list:
            engine_instance = asyncio.run(stockfish_pool.get_stockfish())
            analysis = asyncio.run(analyze_position(engine_instance, fen))
            analysis_results.append(analysis)
            

        print(analysis_results)

        # Step 3: Generate report
        report = generate_report(pgn_data, analysis_results)

        # Combine all results
        result = {
            "positions": [
                {"fen": fen, "analysis": analysis}
                for fen, analysis in zip(fen_list, analysis_results)
            ],
            "report": report
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)