from fastapi import FastAPI, HTTPException
from stockfish import Stockfish
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os

app = FastAPI()

# Create a pool of Stockfish instances
class StockfishPool:
    def __init__(self, pool_size=4, stockfish_path="./stockfish.exe"):
        self.pool = [
            Stockfish(
                path=stockfish_path, 
                depth=17, 
                parameters={"Threads": 1, "Minimum Thinking Time": 10}
            ) 
            for _ in range(pool_size)
        ]
        self.locks = [asyncio.Lock() for _ in range(pool_size)]
        self.semaphore = asyncio.Semaphore(pool_size)

    async def get_stockfish(self):
        async with self.semaphore:
            # Find an available Stockfish instance
            for i, lock in enumerate(self.locks):
                if lock.locked():
                    continue
                async with lock:
                    return self.pool[i]
            raise Exception("No Stockfish instance available")

# Initialize the Stockfish pool
stockfish_pool = StockfishPool(
    pool_size=os.cpu_count() or 4  # Use number of CPU cores
)

class FenRequest(BaseModel):
    fen: str

@app.post("/analyze")
async def analyze_fen(fen_request: FenRequest):
    """API endpoint to analyze a single FEN."""
    # Get an available Stockfish instance
    stockfish = await stockfish_pool.get_stockfish()
    
    # Validate and analyze
    if not stockfish.is_fen_valid(fen_request.fen):
        raise HTTPException(status_code=400, detail="Invalid FEN")

    stockfish.set_fen_position(fen_request.fen)
    best_move = stockfish.get_best_move()
    return {"fen": fen_request.fen, "best_move": best_move}

@app.post("/analyze_bulk")
async def analyze_bulk(fens: list[FenRequest]):
    """API endpoint to analyze multiple FENs."""
    results = []
    
    # Use thread pool for potentially faster processing
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        loop = asyncio.get_event_loop()
        
        async def process_fen(fen_request):
            stockfish = await stockfish_pool.get_stockfish()
            
            if not stockfish.is_fen_valid(fen_request.fen):
                return {"fen": fen_request.fen, "error": "Invalid FEN"}
            
            stockfish.set_fen_position(fen_request.fen)
            best_move = stockfish.get_best_move()
            return {"fen": fen_request.fen, "best_move": best_move}
        
        # Process FENs concurrently
        results = await asyncio.gather(
            *[process_fen(fen_request) for fen_request in fens]
        )
    
    return results