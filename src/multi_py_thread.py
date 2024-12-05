# We are creating 4 threads to process the FENs in parallel. Each thread has a subset of total fens and a stockfish instance. It loops over them until all the evaluations are done. Some Code is ai genearated by the idea is mine any improvemnents and suggestions are welcome.

from stockfish import Stockfish
from utils.fens import fens
import concurrent.futures
import time

# Function to process a subset of FENs and return the best move for each
def process_fens_for_thread(start_idx, end_idx, thread_id):
    # Create a new instance of Stockfish for this thread
    stockfish = Stockfish(path="./src/engine/stockfish.exe", depth=15, parameters={"Threads": 2, "Minimum Thinking Time": 10})
    results = []

    for index in range(start_idx, end_idx):
        fen = fens[index]
        start_time = time.time()
        result = {}

        try:
            # Ensure Stockfish is running and initialized before setting the FEN position
            print(f"Thread {thread_id}: Setting FEN {index + 1}/{len(fens)}: {fen}")
            valid = stockfish.is_fen_valid(fen)
            if valid:
                stockfish.set_fen_position(fen)
                # Get the best move
                best_move = stockfish.get_best_move()
                result['fen'] = fen
                result['best_move'] = best_move
                result['index'] = index
            else:
                result['error'] = f"Invalid FEN: {fen}"
        except Exception as e:
            result['error'] = str(e)

        # Time evaluation and progress
        elapsed_time = time.time() - start_time
        progress = ((index + 1) / len(fens)) * 100

        # Print progress every 10% interval
        if progress % 10 == 0 or progress == 100:
            print(f"Thread {thread_id}: Progress: {progress:.0f}% done, Time elapsed: {elapsed_time:.2f} seconds")

        results.append(result)

    return results

# Function to handle the threads and distribute FENs
def process_fens_in_parallel(fens):
    total_fens = len(fens)
    num_threads = 4
    results = []

    # Calculate the range of FENs for each thread
    chunk_size = total_fens // num_threads
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_threads)]
    chunks[-1] = (chunks[-1][0], total_fens)  # Make sure the last thread gets the remaining FENs

    # Start a ThreadPoolExecutor with 4 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_chunk = {executor.submit(process_fens_for_thread, start, end, idx): (start, end) for idx, (start, end) in enumerate(chunks)}

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_chunk):
            result = future.result()
            results.extend(result)  # Append results for this chunk to the overall results

    return results

# Start the processing
start_time = time.time()

results = process_fens_in_parallel(fens)

elapsed_time = time.time() - start_time
print(f"Total time elapsed: {elapsed_time:.2f} seconds")
print(f"Processed {len(results)} FENs.")