
async def analyze_position(stockfish, fen):
    stockfish.set_fen_position(fen)

    top_lines = stockfish.get_top_moves(num_top_moves=2)
    evaluation = stockfish.get_evaluation()


    if(top_lines == []): # Means it was a mate
       return {
            "evaluation": "1 - 0",
            "mate": True,
            "top_lines": top_lines,
            "depth": 20
       }
 
    return {
        "evaluation": evaluation,
        "top_lines": top_lines,
        "depth": 20
    }