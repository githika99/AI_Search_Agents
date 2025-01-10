import chess
import random
from math import inf
from IPython.display import display, clear_output

MAX_DEPTH = 3
SEED = random.Random(0)  # Feel free to set/reset the seed for testing purposes!

def evaluation(board: chess.Board, player: bool):
    """
    This function evaluates a board position and returns a score value.
    
    Parameters:
    - board: the chess board
    - player: the colour of the active player (True -> white, False -> black)
    
    Returns:
    - an integer score for a board state
    """
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
        return white_score-black_score  + (len(white_legal_moves)-len(black_legal_moves)) 
    
    return black_score-white_score + (len(black_legal_moves)-len(white_legal_moves))  


def get_expectimax_move(board: chess.Board, player: bool, depth: int):   
    """
    This function chooses the best move for the given board position, player, and depth.
    
    Parameters:
    - board: the chess board that the knight is moving upon
    - player: the colour of the active player (True -> white, False -> black)
    - depth: the number of moves that the algorithmn should look ahead.
    
    Returns:
    A single chess.Move type object.
    """
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

    #print("outside any node")
    #display(board)
    def max_node(local_b, local_player, local_depth):
        if local_b.is_checkmate(): # white checkmate
            return float('inf') 
        # elif local_b.is_stalemate() or local_b.can_claim_draw():
        #     float('-inf') 
        #print("In max node, depth", local_depth)
        if local_depth == 0: #return eval function for white
            #print("at leaf, returning eval score", evaluation(local_b, local_player))
            return evaluation(local_b, local_player)
        v = float('-inf')
        #print("white's turn")
        curr_turn = chess.WHITE
    
        for move in move_ordering(local_b):
            local_b.turn = curr_turn
            local_b.push(move)
            #print("just tried a move, going to min_node")
            #display(local_b)
            v = max(v, exp_node(local_b, not local_player, local_depth-1))            
            #undo move
            local_b.pop()
            #print("back in max_node, undoing that move, depth", local_depth)
            #display(local_b)
        #print("returning v of", v)
        if local_depth == depth:
            #print("Final move for white is", move)
            return move
        return v

    def exp_node(local_b, local_player, local_depth):
        if local_b.is_checkmate(): # black checkmate
            return float('-inf') 
        # elif local_b.is_stalemate() or local_b.can_claim_draw():
        #     return v
        #print("In exp node, depth", local_depth)
        if local_depth == 0: #return eval function for black
            #print("at leaf, returning eval score", evaluation(local_b, local_player))
            return evaluation(local_b, local_player)
        v = 0
        #print("black's turn")
        curr_turn = chess.BLACK
        moves = move_ordering(local_b)
        for move in moves:
            local_b.turn = curr_turn
            local_b.push(move)
            #print("just tried a move, going to max_node")
            #display(local_b)
            p = 1/len(moves)
            v += p * max_node(local_b, not local_player, local_depth-1)
            local_b.pop()
            
            #print("back in exp_node, undoing that move, depth", local_depth)
            #display(local_b)
        #print("returning v of", v)
        return v
    
    return max_node(board, player, depth)

def get_random_move(b:chess.Board, *_):
    return SEED.choice(list(b.legal_moves))

def grade_game(p1, p2):
    """
    Grades a single game at a time.
    (Note: differs from actual grading script, which has some ways to resolve draws.)

    Return legend:
    0: error during game
    1: p1 wins through checkmate
    2: p2 wins through checkmate
    3: draw
    """
    board = chess.Board()
    current_player = p1

    while not board.is_checkmate() and not board.is_stalemate() and not board.can_claim_draw():
        move = current_player(board, board.turn, MAX_DEPTH)
        try:
            board.push(move)
        except:            
            print(f"Error while grading game, move = {move}, current_player = {current_player}")
            print(board)
            return -1

        current_player = p1 if board.turn else p2
    
    outcome = board.outcome()
    if outcome is not None:
        if outcome.winner:
            return 1
        else:
            return 2
    
    return 3

random_agent = get_random_move
best_agent = get_expectimax_move
num_games = 5

print(f"Playing {num_games} games...")
for i in range(1, num_games+1):
    result = grade_game(best_agent, random_agent)

    if result == 0:
        print(f"Game {i}: error pushing a move during gameplay")
        
    elif result == 1:
        print(f"Game {i}: p1 wins")
        
    elif result == 2:
        print(f"Game {i}: p1 loses")
    
    elif result == 3:
        print(f"Game {i}: draw")