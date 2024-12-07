
async def analyze_position(stockfish, fen, depth=17):
    stockfish.set_fen_position(fen)

    top_lines = stockfish.get_top_moves(num_top_moves=2)

    if(top_lines == []): # Means it was a mate
       return {
            "mate": True,
            "top_lines": top_lines,
            "depth": depth
       }
 
    return {
        "top_lines": top_lines,
        "depth": depth
    }