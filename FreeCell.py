import random
from cs1graphics import *

IMG_PATH = './images/'

SUIT_NAMES = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
FACE_NAMES = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
GAME_BOARD = Canvas(680, 600, 'dark green', 'FreeCell')
MOVE_STACK = []

# global message box
message = Text("Welcome to FreeCell!", centerPt=Point(340, 580))
message.setFontColor("white")
commands = Text("undo(Backspace)  restart(R)  auto-sort(A)", centerPt=Point(340, 10))
commands.setFontColor("white")

# toggle options
OPT_AUTOSORT = True # auto-sort

"""
Define the Card class
"""
class Card:
    """Information for card"""
    def __init__(self):
        self.face = ""
        self.suit = ""
        self.face_num = 0
        self.color = ""
    
    def __str__(self):
        return f"<{self.color} {self.face}>"


def create_deck(deckID = 0):
    """
    Create a list("deck") of all 52 cards, shuffle them and return the list.
    """
    deck = []
    
    if not deckID: # Random Shuffle
        for i in range(4):
            for j in range(13):
                img = Image('./cards/' + SUIT_NAMES[i] + '_' + FACE_NAMES[j]+ '.png')
                card = Card()
                card.face = FACE_NAMES[j]
                card.face_num = j
                card.suit = SUIT_NAMES[i]
                card.image = img
                card.state = True
                card.pick = 0
                card.id = 13*i + j

                if card.suit in ['Clubs', 'Spades']:
                    card.color = 'black'
                else:
                    card.color = 'red'

                deck.append(card)
        
        random.shuffle(deck)
        for card in deck:
            deckID += card.id
            deckID *= 52
        
        deckID = hex(deckID)
    
    else: # Make User Deck
        pass

    return deck, deckID

def update_card(decks):
    """
    Update card drawn on the canvas.
    """

    x0, y0 = 50, 75
    x1, y1 = 400, 75
    x2, y2 = 50, 200

    GAME_BOARD.clear()

    # basic elements
    GAME_BOARD.add(message)
    GAME_BOARD.add(commands)

    # counter
    counter = Text(f"move : {len(MOVE_STACK)}", centerPt=Point(640, 580))
    counter.setFontColor("white")
    GAME_BOARD.add(counter)
    
    dx = 0
    for card in decks[True][:4]:
        if card:
            card[-1].image.moveTo(x0 + dx, y0 - card[-1].pick)
            GAME_BOARD.add(card[-1].image)
        else:
            GAME_BOARD.add(Rectangle(72, 100, Point(x0 + dx, y0)))

        dx += 75
    
    dx = 0
    for card in decks[True][4:]:
        if card:
            card[-1].image.moveTo(x1 + dx, y1 - card[-1].pick)
            GAME_BOARD.add(card[-1].image)
        else:
            GAME_BOARD.add(Rectangle(72, 100, Point(x1 + dx, y1)))

        dx += 75
    
    dx, dy = 0, 0 
    for deck in decks[False]:
        if deck:
            for card in deck:
                card.image.moveTo(x2 + dx, y2 + dy - card.pick)
                GAME_BOARD.add(card.image)
                dy += 20
        else:
            GAME_BOARD.add(Rectangle(72, 100, Point(x2 + dx, y2 + dy)))

        dx += 75
        if dx == 300:
            dx += 50
        dy = 0

def select_card(decks):
    while True:
        wait = GAME_BOARD.wait()

        if wait.getDescription() == "mouse click":
            x, y = wait.getMouseLocation().get()

            index = -1
            if x < 312:
                index = int((x - 13) // 75)
            elif x > 363:
                index = int((x - 63) // 75)

            if index in range(8):
                point = max(200, 180 + len(decks[False][index]) * 20)
                if int(y) in range(point - 50, point + 50):
                    return index, False
                elif int(y) in range(25, 125):
                    return index, True
                
        elif wait.getDescription() == "keyboard":
            key = wait.getKey()

            if key == '\b': # undo
                decks = undo_cards(decks)

            if key == 'r': # restart
                print("restart")
                pass
                
            if key == 'a': # auto-sort
                global OPT_AUTOSORT
                OPT_AUTOSORT = not OPT_AUTOSORT
                switch = ['off', 'on']
                message.setMessage(f"auto-sort option: {switch[OPT_AUTOSORT]}.")

def move_card(decks, moveFrom, moveTo, undo=False):
    decks[moveFrom[1]][moveFrom[0]][-1].pick = 0
    decks[moveTo[1]][moveTo[0]].append(decks[moveFrom[1]][moveFrom[0]].pop())

    if moveFrom != moveTo and not undo:
        MOVE_STACK.append((moveFrom, moveTo))

    update_card(decks)
    return decks

def autosort_card(decks):
    for column, cards in enumerate(decks[False]): # check decks
        if len(cards) == 0:
            continue
        for index, suit in enumerate(SUIT_NAMES):
            if cards[-1].suit == suit and \
                (not (decks[True][4+index] or cards[-1].face_num) or \
                (decks[True][4+index] and cards[-1].face_num == decks[True][4+index][-1].face_num + 1)):
                decks = move_card(decks, (column, False), (4+index, True))
                decks = autosort_card(decks)
                break
    
    for column, cards in enumerate(decks[True][:4]): # check free cells
        if len(cards) == 0:
            continue
        for index, suit in enumerate(SUIT_NAMES):
            if cards[-1].suit == suit and \
                (not (decks[True][4+index] or cards[-1].face_num) or \
                (decks[True][4+index] and cards[-1].face_num == decks[True][4+index][-1].face_num + 1)):
                decks = move_card(decks, (column, True), (4+index, True))
                decks = autosort_card(decks)
                break
    
    return decks

def undo_cards(decks):
    if MOVE_STACK:
        moveTo, moveFrom = MOVE_STACK.pop()
        decks = move_card(decks, moveFrom, moveTo, undo=True)
    
    else:
        message.setMessage("You cannot undo from the initial board.")
    
    return decks

# START MAIN PROGRAM
if __name__ == "__main__":

    deque = []

    # prompt for starting a new game and create a deck
    print ("Welcome to FreeCell!\n")
    deque, deckID = create_deck()

    # create two hands of dealer and player
    cell = [list() for i in range(8)]
    decks = [[list() for i in range(8)], cell]
    attack = 0
    seven = False

    # initiate decks
    for i in range(7):
        for deck in decks[False]:
            if not deque:
                break
            deck.append(deque.pop())

    update_card(decks)
    selected = False

    # do infinite loop until game ends
    while True:
        index, isCell = select_card(decks)
        if selected:
            moveTo = index, isCell
            if isCell and index < 4: # free cell
                if not decks[isCell][index]:
                    decks = move_card(decks, moveFrom, moveTo)
                    message.setMessage("")
                else:
                    decks = move_card(decks, moveFrom, moveFrom)
                    message.setMessage("You cannot move card to non-empty free cell!")
            elif isCell and index >= 4: # home cell
                if decks[moveFrom[1]][moveFrom[0]][-1].suit == SUIT_NAMES[index - 4] and \
                    (not (decks[isCell][index] or decks[moveFrom[1]][moveFrom[0]][-1].face_num) or\
                    (decks[isCell][index] and decks[moveFrom[1]][moveFrom[0]][-1].face_num == decks[isCell][index][-1].face_num + 1)):
                    decks = move_card(decks, moveFrom, moveTo)
                    message.setMessage("")
                else:
                    decks = move_card(decks, moveFrom, moveFrom)
                    message.setMessage("Wrong move! Card at home cell must be organized from A to K.")
            else: # decks
                if not decks[isCell][index] or \
                    (decks[moveFrom[1]][moveFrom[0]][-1].color != decks[isCell][index][-1].color and \
                    decks[moveFrom[1]][moveFrom[0]][-1].face_num + 1 == decks[isCell][index][-1].face_num):
                    decks = move_card(decks, moveFrom, moveTo)
                    message.setMessage("")
                else:
                    decks = move_card(decks, moveFrom, moveFrom)
                    message.setMessage("Wrong move! Card at decks must be organized from K to A and alternating colors.")
            
            if OPT_AUTOSORT:
                decks = autosort_card(decks)

        else:
            if decks[isCell][index] and ((isCell and index < 4) or not isCell): # home cell, empty cell excluded
                decks[isCell][index][-1].pick = -20
                moveFrom = index, isCell
                update_card(decks)
            else: 
                continue

        selected = not selected

        # End condition
        if sum([len(i) for i in decks[True][4:]]) == 52:
            decks = update_card(decks)
            message.setMessage("You Won! Congraturations!")
            break
