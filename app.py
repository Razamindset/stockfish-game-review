from flask import Flask, request, jsonify
from src.utils.parse_pgn import parse_pgn
from src.utils.analyze import analyze_position
from src.utils.generate_report import generate_report
from src.utils.stockfish_pool import StockfishPool
import os
import asyncio
import concurrent.futures
from stockfish import Stockfish
import time


app = Flask(__name__)
THREADS = os.cpu_count() or 4  # Use number of CPU cores
DEPTH = 17

# Initialize the Stockfish pool
stockfish_pool = StockfishPool(
    pool_size = THREADS,
)


def process_fens_for_thread(start_idx, end_idx, thread_id, fen_list):
    #! Accesing the engine from the pool was causing trouble so for new we define a new instance per thread for now
    start_time_to_start_engine = time.time()
    # engine_instance = Stockfish(path="./stockfish.exe", depth=DEPTH, parameters={"Threads": 1, "Minimum Thinking Time": 10, "Hash": 512})

    engine_instance = asyncio.run(stockfish_pool.get_stockfish())
    if(engine_instance == None):
        print("No engine available")
        return []
    results = []
    print("Time taken to spin up engine: ", time.time() - start_time_to_start_engine)

    try:
        for index in range(start_idx, end_idx):
            fen = fen_list[index]
            move_analysis = asyncio.run(analyze_position(engine_instance, fen, DEPTH))
            print(move_analysis)
            results.append(move_analysis)

        return results
    
    except Exception as e:
        print(f"Thread {thread_id}: Error processing FENs: {e}")
        return []


@app.route('/review_game', methods=['POST'])
def review_game():
    pgn_data = request.json.get('pgn')
    

    if not pgn_data:
        return jsonify({"error": "No PGN data provided"}), 400

    try:
        # Step 1: Parse PGN
        fen_list = parse_pgn(pgn_data)

        # Use multiple threads to do analysis side by side

        #! Single threaded approach
        # analysis_results = []
        # for fen in fen_list:
        #     engine_instance = asyncio.run(stockfish_pool.get_stockfish())
        #     analysis = asyncio.run(analyze_position(engine_instance, fen))
        #     analysis_results.append(analysis)

        #! Multi threaded approach
        total_fens = len(fen_list)
        results = []

        # Calculate the range of fens for each thread
        chunkk_size = total_fens // THREADS
        chunks = [(i * chunkk_size, (i + 1) * chunkk_size) for i in range(THREADS)]
        chunks[-1] = (chunks[-1][0], total_fens) # Adjust the last chunk to include the remaining fens
        print(chunks[-1])
        start_time = time.time()


        #! Create a thread pool executor and I understand shit about this
        # Start a ThreadPoolExecutor with 4 threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
            future_to_chunk = {executor.submit(process_fens_for_thread, start, end, idx, fen_list): (start, end) for idx, (start, end) in enumerate(chunks)}
            results = []  # Initialize results list to collect results from futures
            for future in concurrent.futures.as_completed(future_to_chunk):
                result = future.result()
                results.extend(result)  # Append results for this chunk to the overall results
            
        print("Analyzed all positions.", len(results), " in ", time.time() - start_time, " seconds")

        #TODO Step 3: Generate report
        report = generate_report(pgn_data, results)

        # Combine all results
        result = {
            "positions": [
                {"fen": fen, "analysis": analysis}
                for fen, analysis in zip(fen_list, results)
            ],
            "report": report
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)