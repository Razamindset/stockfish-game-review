"Instead of dviding the work among threads, we can use a single thread to process all FENs. This is not the best but is an alternate apporach"

from stockfish import Stockfish
from utils.fens import fens
import time

start_time = time.time()

stockfish = Stockfish(path="./src/engine/stockfish.exe", depth=17, parameters={"Threads": 4, "Minimum Thinking Time": 10})

# Function to calculate and print progress
def calculate_progress(current, total):
    return (current / total) * 100

# Store results
results = []

# Process FENs and calculate progress
try:
    total_fens = len(fens)
    for idx, fen in enumerate(fens):
        # Check if the FEN is valid
        valid = stockfish.is_fen_valid(fen)
        result = {'fen': fen}
        
        if valid:
            stockfish.set_fen_position(fen)
            best_move = stockfish.get_best_move()
            result['best_move'] = best_move
        else:
            result['error'] = f"Invalid FEN: {fen}"
        
        # Append the result to the list
        results.append(result)
        
        # Print progress every 10%
        progress = calculate_progress(idx + 1, total_fens)
        if progress % 5 == 0 or progress == 100:
            print(f"Progress: {progress:.0f}% done")
            
except Exception as e:
    print(f"Error: {e}")


# Display all results at the end
print("\nProcessed Positions: ", len(results), "in ", time.time() - start_time, "seconds")