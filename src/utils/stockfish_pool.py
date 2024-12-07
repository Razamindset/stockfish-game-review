import asyncio
from stockfish import Stockfish

class StockfishPool:
    # ! AI gnerated shitty code handle with intensive care
    def __init__(self, pool_size=4, stockfish_path="./stockfish.exe", depth=17):
        self.pool = [
            Stockfish(
                path=stockfish_path,
                depth=depth,
                parameters={"Threads": 1, "Minimum Thinking Time": 10, "Hash": 128}
            )
            for _ in range(pool_size)
        ]
        self.semaphore = asyncio.Semaphore(pool_size)
        self.locks = [asyncio.Lock() for _ in range(pool_size)]

    #? I will learn this some other day for now it works
    async def get_stockfish(self):
        await self.semaphore.acquire()
        for i, lock in enumerate(self.locks):
            if not lock.locked():
                await lock.acquire()
                return i, self.pool[i]
        raise Exception("No Stockfish instance available")

    def release_stockfish(self, index):
        self.locks[index].release()
        self.semaphore.release()

    async def analyze_position(self, fen, depth=17):
        index, stockfish = await self.get_stockfish()
        try:
            stockfish.set_fen_position(fen)
            top_lines = stockfish.get_top_moves(2)
            
            if not top_lines:
                return {
                    "mate": True,
                    "top_lines": [],
                    "depth": depth
                }
            
            return {
                "top_lines": top_lines,
                "depth": depth
            }
        finally:
            self.release_stockfish(index)