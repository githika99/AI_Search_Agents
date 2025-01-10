import chess
import random
from math import inf
from IPython.display import display, clear_output

MAX_DEPTH = 3
SEED = random.Random(998)  # Feel free to set/reset the seed for testing purposes!

def evaluation(board: chess.Board, player: bool):
    """
    This function evaluates a board position and returns a score value.
    
    Parameters:
    - board: the chess board
    - player: the colour of the active player (True -> white, False -> black)
    
    Returns:
    - an integer score for a board state
    """
    # CITE: Pawn Structure code was taken from ____
    # Pawn Structure
    # white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    # black_pawns = board.pieces(chess.PAWN, chess.BLACK)

    # doubled_pawns = {"white": 0, "black": 0}
    # blocked_pawns = {"white": 0, "black": 0}
    # isolated_pawns = {"white": 0, "black": 0}

    # # Check for doubled and isolated pawns for both colors
    # for color, pawns in [("white", white_pawns), ("black", black_pawns)]:
    #     files = [chess.square_file(sq) for sq in pawns]  # File indices for pawns
    #     unique_files = set(files)

    #     # Doubled pawns: More than one pawn on the same file
    #     for file in unique_files:
    #         count = files.count(file)
    #         if count > 1:
    #             doubled_pawns[color] += count - 1  # Number of additional pawns on that file

    #     # Isolated pawns: No friendly pawns on adjacent files
    #     for sq in pawns:
    #         file = chess.square_file(sq)
    #         if not any(chess.square_file(p) in {file - 1, file + 1} for p in pawns):
    #             isolated_pawns[color] += 1

    # Check for blocked pawns
    # for color, pawns in [("white", white_pawns), ("black", black_pawns)]:
    #     direction = 8 if color == "white" else -8  # White pawns move +8, black pawns move -8
    #     for sq in pawns:
    #         front_sq = sq + direction
    #         if chess.SQUARES[0] <= front_sq < 64:  # Ensure the front square is valid
    #             front_piece = board.piece_at(front_sq)
    #             # Check if the front piece is an opponent’s piece or any piece blocking the pawn
    #             if front_piece is not None and front_piece.color != color:
    #                 blocked_pawns[color] += 1
    
    # End of Pawn Structure

    # pawn - 10, knight - 30, bishop - 30, rook - 50, queen - 90, king - 900
    white_score = len(board.pieces(chess.PAWN, chess.WHITE)) * 10 + len(board.pieces(chess.KNIGHT, chess.WHITE)) * 30 + len(board.pieces(chess.BISHOP, chess.WHITE)) * 30 + len(board.pieces(chess.ROOK, chess.WHITE)) * 50 + len(board.pieces(chess.QUEEN, chess.WHITE)) * 90 + len(board.pieces(chess.KING, chess.WHITE)) * 900

    black_score = len(board.pieces(chess.PAWN, chess.BLACK)) * 10 + len(board.pieces(chess.KNIGHT, chess.BLACK)) * 30 + len(board.pieces(chess.BISHOP, chess.BLACK)) * 30 + len(board.pieces(chess.ROOK, chess.BLACK)) * 50 + len(board.pieces(chess.QUEEN, chess.BLACK)) * 90 + len(board.pieces(chess.KING, chess.BLACK)) * 900

    curr_turn = board.turn

    board.turn = chess.WHITE  # Set the turn to the desired color
    white_legal_moves = list(board.legal_moves)  # Get all legal moves
    board.turn = chess.BLACK  # Set the turn to the desired color
    black_legal_moves = list(board.legal_moves)  # Get all legal moves

    # set the turn back
    board.turn = curr_turn

    if player:  #white
        return white_score-black_score  + (len(white_legal_moves)-len(black_legal_moves))  #- 5 * (blocked_pawns["white"] - blocked_pawns["black"] + isolated_pawns["white"] - isolated_pawns["black"] + doubled_pawns["white"] - doubled_pawns["black"])
    
    return black_score-white_score + (len(black_legal_moves)-len(white_legal_moves))  #- 5 * (blocked_pawns["black"] - blocked_pawns["white"] + isolated_pawns["black"] - isolated_pawns["white"] + doubled_pawns["black"] - doubled_pawns["white"])
    

def move_ordering(board):
    """Order moves based on captures and checks for better pruning."""
    def move_score(move):
        # Capture score: prioritize capturing higher-value pieces with lower-value ones
        if board.is_capture(move) and board.piece_at(move.from_square) and board.piece_at(move.to_square):
            captured_piece = board.piece_at(move.to_square)
            attacker_piece = board.piece_at(move.from_square)
            return (captured_piece.piece_type * 10) - attacker_piece.piece_type
        elif board.gives_check(move):
            return 5  # Prioritize moves that give check
        return 0  # Non-capturing, non-checking moves have lowest priority

    # Sort moves in descending order of their score
    return sorted(board.legal_moves, key=move_score, reverse=False)


def get_minimax_move(board: chess.Board, player: bool, depth: int):   
    """
    This function chooses the best move for the given board position, player, and depth.
    
    Parameters:
    - board: the chess board that the knight is moving upon
    - player: the colour of the active player (True -> white, False -> black)
    - depth: the number of moves that the algorithmn should look ahead.
    
    Returns:
    A single chess.Move type object.
    """

    # print("outside any node")
    # display(board)
    def max_node(local_b, local_player, local_depth, a, b):
        # print("In max node, depth", local_depth)
        if local_depth == 0: #return eval function for white
            # print("at leaf, returning eval score", evaluation(local_b, local_player))
            return evaluation(local_b, local_player)
        v = float('-inf')
        # if local_player: # True = White
            # print("white's turn")
        curr_turn = chess.WHITE
        # else:
        #     # print("black's turn")
        #     curr_turn = chess.BLACK
        #for move in local_b.legal_moves:
        for move in move_ordering(local_b):
            local_b.turn = curr_turn
            local_b.push(move)
            # print("just tried a move, going to min_node")
            # display(local_b)
            v = max(v, min_node(local_b, not local_player, local_depth-1, a, b))
            a = max(a, v)
            if a >= b:
                # print("returning v of", v)
                local_b.pop()
                if local_depth == depth:
                    print("Final move for white is", move)
                    return move
                return v
            #undo move
            local_b.pop()
            # print("back in max_node, undoing that move, depth", local_depth)
            # display(local_b)
        # print("returning v of", v)
        if local_depth == depth:
            print("Final move for white is", move)
            return move
        return v

    def min_node(local_b, local_player, local_depth, a, b):
        # print("In min node, depth", local_depth)
        if local_depth == 0: #return eval function for black
            # print("at leaf, returning eval score", evaluation(local_b, local_player))
            return evaluation(local_b, local_player)
        v = float('inf')
        # if local_player: # True = White
        #     # print("white's turn")
        #     curr_turn = chess.WHITE
        # else:
            # print("black's turn")
        curr_turn = chess.BLACK
        #for move in local_b.legal_moves:
        for move in move_ordering(local_b):
            local_b.turn = curr_turn
            local_b.push(move)
            # print("just tried a move, going to max_node")
            # display(local_b)
            v = min(v, max_node(local_b, not local_player, local_depth-1, a, b))
            b = min(b, v)
            if a >= b:
                # print("returning v of", v)
                local_b.pop()
                return v
            #undo move
            local_b.pop()
            # print("back in min_node, undoing that move, depth", local_depth)
            # display(local_b)
        # print("returning v of", v)
        return v
    
    return max_node(board, player, depth, a=float('-inf'), b=float('inf'))


def get_random_move(b:chess.Board, *_):
    return SEED.choice(list(b.legal_moves))


def get_game_result(board):
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"  # Last turn won
        return f"{winner} wins by checkmate!"
    elif board.is_stalemate():
        return "The game is a draw by stalemate."
    elif board.is_insufficient_material():
        return "The game is a draw due to insufficient material."
    elif board.is_repetition():
        return "The game is a draw by repetition."
    elif board.is_fifty_moves():
        return "The game is a draw by the 50-move rule."
    elif board.can_claim_draw():
        return "Can claim draw."
    else:
        return "The game is still ongoing."

def test_game(p1, p2):
    """
    A function that plays a chess game with visuals
    
    Parameters:
    - p1: the first chess agent, playing as the white player
    - p2: the second chess agent, playing as the black player
    
    Returns:
    Nothing, just plays the game one move at a time.
    Press enter in the popup box to play the next move.
    Type 'q' into the popup box and press enter to stop the game (you can also interrupt the kernel if this fails.)
    """
    board = chess.Board()
    current_player = p1
    count = 0
    # testing only for one move each
    while count < 5 not board.is_checkmate() and not board.is_stalemate() and not board.can_claim_draw():
        #clear_output(True)
        
        if board.turn:
            print("\nTurn is white")

        else:
            print("\nTurn is black")
        move = current_player(board, board.turn, MAX_DEPTH)
        print("Move is", move)
        board.push(move)
        display(board)
        count += 1
        current_player = p1 if board.turn else p2

        # if input() == "q":
        #     break
    print("final eval score for white", evaluation(board, True))
    print("total moves for both players", count, "total turns", count//2)
    print(get_game_result(board))
    


if __name__ == "__main__":
    # Random Vs. Minimax
    random_agent = get_random_move
    minimax_agent = get_minimax_move
    test_game(minimax_agent, random_agent)
