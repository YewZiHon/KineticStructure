import chess
import chess.svg
import time
import sys

import tkinter as tk
import tksvg

window = tk.Tk()

board = chess.Board()

svgstr = chess.svg.board(
    board,
    size=400)

svg_image = tksvg.SvgImage( data = svgstr )

# You can also resize the image, but using only one of the three available parameters:
# svg_image = tksvg.SvgImage( data = d, scale = 0.5 )
# svg_image = tksvg.SvgImage( data = d, scaletowidth = 200 )
#svg_image = tksvg.SvgImage( data = d, scaletoheight = 200 )

tk.Label( image = svg_image ).pack()
window.mainloop()