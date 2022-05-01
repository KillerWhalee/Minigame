from cs1graphics import *
import random

class newGame:
    def __init__(self, width, height, mine) -> None:
        
        self.minelist = []
        for i in range(width):
            justlist = []
            for j in range(height):
                justlist.append(0)
            self.minelist.append(justlist)

        # drawing gameboard
        self.gameboard = Canvas(40 + 30 * width, 40 + 30 * height, (120, 120, 120), "MineSweeper")

        for w in range(width + 1):
            line = Path(Point(20 + 30 * w, 20), Point(20 + 30 * w, 20 + 30 * height))
            self.gameboard.add(line)
        
        for h in range(height + 1):
            line = Path(Point(20, 20 + 30 * h), Point(20 + 30 * width, 20 + 30 * h))
            self.gameboard.add(line)

        

        pass

game = newGame(10, 10, 2)
