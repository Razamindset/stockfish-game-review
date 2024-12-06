import chess.pgn
import io

def parse_pgn(pgn_data):
    pgn_io = io.StringIO(pgn_data)
    game = chess.pgn.read_game(pgn_io)
    
    if game is None:
        raise ValueError("Invalid PGN format")

    fen_list = []
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        fen_list.append(board.fen())

    return fen_list