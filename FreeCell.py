import random
from cs1graphics import *

img_path = './images/'

suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
face_names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
gameboard = Canvas(680, 600, 'dark green', 'FreeCell')


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
        return f"<{self.color} {self.face_num}>"


def create_deck(number = 1):
    """
    Create a list("deck") of all 52 cards, shuffle them and return the list.
    """
    deck = []
    
    for i in range(4):
        for j in range(13):
            img = Image('./cards/' + suit_names[i] + '_' + face_names[j]+ '.png')
            card = Card()
            card.face = face_names[j]
            card.face_num = j
            card.suit = suit_names[i]
            card.image = img
            card.state = True
            card.pick = 0

            if card.suit in ['Clubs', 'Spades']:
                card.color = 'black'
            else:
                card.color = 'red'

            deck.append(card)
    
    random.shuffle(deck)

    return deck

def update_card(decks):
    """
    Update card drawn on the canvas.
    """
    depth = 100
    x0, y0 = 50, 75
    x1, y1 = 400, 75
    x2, y2 = 50, 200

    gameboard.clear()
    
    dx = 0
    for card in decks[True][:4]:
        if card:
            card[-1].image.moveTo(x0 + dx, y0 - card[-1].pick)
            gameboard.add(card[-1].image)
        else:
            gameboard.add(Rectangle(72, 100, Point(x0 + dx, y0)))
        dx += 75
    
    dx = 0
    for card in decks[True][4:]:
        if card:
            card[-1].image.moveTo(x1 + dx, y1 - card[-1].pick)
            gameboard.add(card[-1].image)
        else:
            gameboard.add(Rectangle(72, 100, Point(x1 + dx, y1)))
        dx += 75
    
    dx, dy = 0, 0 
    for deck in decks[False]:
        for card in deck:
            card.image.moveTo(x2 + dx, y2 + dy - card.pick)
            gameboard.add(card.image)
            dy += 20
        
        dx += 75
        if dx == 300:
            dx += 50

        dy = 0

def select_card(decks):
    while True:
        wait = gameboard.wait()
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

def move_card(decks, moveFrom, moveTo):
    decks[moveFrom[1]][moveFrom[0]][-1].pick = 0
    decks[moveTo[1]][moveTo[0]].append(decks[moveFrom[1]][moveFrom[0]].pop())
    update_card(decks)
    return decks

def main():

    deque = []

    # prompt for starting a new game and create a deck
    print ("Welcome to FreeCell!\n")
    deque = create_deck()

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
                else:
                    decks = move_card(decks, moveFrom, moveFrom)
            elif isCell and index >= 4: # home cell
                if decks[moveFrom[1]][moveFrom[0]][-1].suit == suit_names[index - 4] and \
                    (not (decks[isCell][index] or decks[moveFrom[1]][moveFrom[0]][-1].face_num) or\
                    decks[moveFrom[1]][moveFrom[0]][-1].face_num == decks[isCell][index][-1].face_num + 1):
                    decks = move_card(decks, moveFrom, moveTo)
                else:
                    decks = move_card(decks, moveFrom, moveFrom)
            else: # decks
                if not decks[isCell][index] or \
                    (decks[moveFrom[1]][moveFrom[0]][-1].color != decks[isCell][index][-1].color and \
                    decks[moveFrom[1]][moveFrom[0]][-1].face_num + 1 == decks[isCell][index][-1].face_num):
                    decks = move_card(decks, moveFrom, moveTo)
                else:
                    decks = move_card(decks, moveFrom, moveFrom)

        else:
            if decks[isCell][index] and ((isCell and index < 4) or not isCell): # home cell, empty cell excluded
                decks[isCell][index][-1].pick = -20
                moveFrom = index, isCell
                update_card(decks)
            else: 
                continue

        selected = not selected

main()
