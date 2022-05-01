from cs1graphics import *
from playsound import playsound

class newGame:
    def __init__(self) -> None:
        ## Variable Set
        self.toggle = False # toggle: black(False), white(True)
        self.gridlist = []
        self.maxrow = [0, 0] # maxrow: [<black>, <white>]

        self.cursor = Polygon(Point(800, 800), Point(800, 810), Point(810, 800))
        self.cursor.setDepth(10)
        

        for i in range(19):
            justlist = []
            for j in range(19):
                justlist.append(0)
            self.gridlist.append(justlist)

        ## Drawing gameboard
        self.gameboard = Canvas(790, 790, (250, 200, 120), 'Omok')
        self.gameboard.add(self.cursor)

        # Horizontal Line
        for i in range(19):
            line = Path()
            start = Point(40 + 40 * i, 40)
            end = Point(40 + 40 * i, 760)
            line.addPoint(start)
            line.addPoint(end)
            self.gameboard.add(line)
        # Horizontal Label
        for i in range(19):
            text = Text(str(i + 1), 12, Point(40 + 40 * i, 20))
            self.gameboard.add(text)

        # Vertical Line
        for i in range(19):
            line = Path()
            start = Point(40, 40 + 40 * i)
            end = Point(760, 40 + 40 * i)
            line.addPoint(start)
            line.addPoint(end)
            self.gameboard.add(line)
        # Vertical Label
        for i in range(19):
            label = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            text = Text(str(label[i]), 12, Point(20, 40 + 40 * i))
            self.gameboard.add(text)

        # Index Dot
        for i in range(3):
            for j in range(3):
                dot = Circle(3, Point(160 + 240 * i, 160 + 240 * j))
                dot.setFillColor("Black")
                self.gameboard.add(dot)


    def locate_calc(self, coord):
        grid = (coord - 20) // 40
        stdv = (((coord - 20) % 40) - 20) ** 2
        
        return grid, stdv
    
    def locate(self, coord):
        # Coord: exact coordinate where mouse have been clicked
        vert, hori = coord
        vert_grid, vert_stdv = self.locate_calc(vert)
        hori_grid, hori_stdv = self.locate_calc(hori)
        vert_grid, hori_grid = int(vert_grid), int(hori_grid)

        # Vaildity check
        if vert_stdv > 50 or hori_stdv > 50:
            return None
        
        if self.gridlist[vert_grid][hori_grid]:
            return None

        return vert_grid, hori_grid

    def put(self, location):
        # Location: processed tuple which contains row(0 ~ 18) and column(0 ~ 18) number
        vert_grid , hori_grid = location

        # Put stone on board
        stone = Circle(16, Point(vert_grid * 40 + 40, hori_grid * 40 + 40))
        stone.setDepth(20)
        if not self.toggle:
            stone.setFillColor("black")
            self.cursor.setFillColor("DarkGreen")
            self.cursor.setBorderColor("White")
        else:
            stone.setFillColor("white")
            self.cursor.setFillColor("Orange")
            self.cursor.setBorderColor("Black")

        self.gameboard.add(stone)
        # playsound("./resources/ttuk.mp3")

        # Save grid datalist
        beadcolor = 1
        if not self.toggle:
            beadcolor *= -1
        # beadcolor: white(1) black(-1)
        self.gridlist[vert_grid][hori_grid] = beadcolor

        # Indicate stone using cursor
        self.cursor.moveTo(vert_grid * 40 + 40, hori_grid * 40 + 40)
    
    def check(self, location):
        beadcolor = 1
        maxrowindex = 1
        if not self.toggle:
            beadcolor *= -1
            maxrowindex = 0

        checker = [1, 1, 1, 1]

        incr = [1, 1, 1, 0, -1, -1, -1, 0]
        incr_vert, incr_hori = 0, -2

        for direction in range(8):
            vert_grid , hori_grid = location
            counter = -1

            while self.gridlist[vert_grid][hori_grid] == beadcolor:
                counter += 1
                vert_grid += incr[incr_vert]
                hori_grid += incr[incr_hori]
                
                if vert_grid > 18 or hori_grid > 18:
                    break
                if vert_grid < 0 or hori_grid < 0:
                    break
            
            checker[direction % 4] += counter

            incr_vert += 1
            incr_hori += 1
        
        for count in checker:
            if count > self.maxrow[maxrowindex]:
                self.maxrow[maxrowindex] = count
        
## Main
board = newGame()

while True:
    queue = board.gameboard.wait()

    eventType = queue.getDescription()
    if eventType != "mouse click":
        continue
    
    coordinate = queue.getMouseLocation().get()
    location = board.locate(coordinate)

    if location:
        board.put(location)
        board.check(location)

        # Toggle player
        board.toggle = not board.toggle
    
    if board.maxrow[0] >= 5:
        print("Black Won the Game!")
        break
    elif board.maxrow[1] >= 5:
        print("White Won the Game!")
        break
