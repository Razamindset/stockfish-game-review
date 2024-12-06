from stockfish import Stockfish
import asyncio

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