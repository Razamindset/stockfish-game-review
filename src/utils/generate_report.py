
def generate_report(pgn_data, analysis_results):
    moves = len(analysis_results)
    
    return {
        "total_moves": moves,
        "summary": f"The game consisted of {moves} moves"
    }