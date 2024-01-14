import serialHelper
import chess
import stockfish

class chessbot():
    def __init__(self):
        self.board = chess.Board()


if __name__ =="__main__":
    
    tc1,board = serialHelper.init()
    if not tc1 or not board:
        raise Exception("Not connected: (tc1, board)",tc1,board)
    tc1 = serialHelper.printerHandle(tc1)
    board = serialHelper.boardHandle(board)