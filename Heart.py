import random
import time
from cs1graphics import *

img_path = './images/'

suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
face_names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']



gameboard = Canvas(600, 400, 'dark green', 'Heart')


"""
Define the Card class
"""
class Card:
    """Information for card"""
    pass

class Player:
    """Information for player"""
    def __init__(self):
        self.cards = []
        self.suitindex = {'Clubs': 0, 'Diamonds': 0, 'Hearts': 0, 'Spades': 0}
        self.taken = []
        self.round = 0
        self.score = 0
        self.firstturn = False

def create_deck():
    """
    Create a list("deck") of all 52 cards, shuffle them and return the list.
    """
    deck = []
    code = 0
    
    for i in range(4):
        for j in range(13):
            img = Image('./cards/' + suit_names[i] + '_' + face_names[j]+ '.png')
            card = Card()
            card.face = face_names[j]
            card.suit = suit_names[i]
            card.code = code
            code += 1
            
            card.value = 0
            if card.suit == 'Hearts':
                card.value == 1
            if card.suit == 'Spades' and card.face == 'Queen':
                card.value == 13
            
            card.image = img
            card.state = True
            card.pick = 0
            deck.append(card)
    
    random.shuffle(deck)

    return deck
    

def select(playerlist):
    """
    Select card player want to draw.
    """
    index = 0
    playerlist[0].cards[0].pick = 20
    update_card(playerlist)
    
    while True:
        wait = gameboard.wait()
        keytype = wait.getDescription()
        if keytype == 'keyboard':
            keyinput = wait.getKey()
            if keyinput == 'a':
                if index == 0:
                    playerlist[0].cards[index].pick = 0
                    index = len(playerlist[0].cards) - 1
                    playerlist[0].cards[index].pick = 20
                else:
                    playerlist[0].cards[index].pick = 0
                    index -= 1
                    playerlist[0].cards[index].pick = 20
                
                update_card(playerlist)
            elif keyinput == 'd':
                if index == len(playerlist[0].cards) - 1:
                    playerlist[0].cards[index].pick = 0
                    index = 0
                    playerlist[0].cards[index].pick = 20
                else:
                    playerlist[0].cards[index].pick = 0
                    index += 1
                    playerlist[0].cards[index].pick = 20
                
                update_card(playerlist)
            elif keyinput == 'w':
                playerlist[0].cards[index].pick = 0
                return index


def player_AI(playerlist, drawn, id, strategy = None):
    """
    Select optimal card to draw.
    It depends on player's strategy.
    """
    pass


def update_card(playerlist, drawn = [None, None, None, None]):
    """
    Update card drawn on the canvas.
    """
    depth = 100
    x0, y0 = 200, 400
    x1, y1 = 600, 300
    x2, y2 = 400, 0
    x3, y3 = 0, 100

    xd0, yd0 = 200, 200
    xd1, yd1 = 300, 300
    xd2, yd2 = 400, 200
    xd3, yd3 = 300, 100

    gameboard.clear()
    
    delta = 0
    for cards in playerlist[0].cards:
        cards.image.moveTo(x0 + delta, y0 - cards.pick)
        gameboard.add(cards.image)
        delta += 15

    delta = 0
    for cards in playerlist[1].cards:
        Back = Image('./cards/Back_rotate.png')
        Back.moveTo(x1, y1 - delta)
        gameboard.add(Back)
        delta += 15
    
    delta = 0
    for cards in playerlist[2].cards:
        Back = Image('./cards/Back.png')
        Back.moveTo(x2 - delta, y2)
        gameboard.add(Back)
        delta += 15
    
    delta = 0
    for cards in playerlist[3].cards:
        Back = Image('./cards/Back_rotate.png')
        Back.moveTo(x3, y3 + delta)
        gameboard.add(Back)
        delta += 15

    if drawn[0]:
        drawn[0].image.moveTo(xd0, yd0)
        gameboard.add(drawn[0].image)
    if drawn[1]:
        drawn[1].image.moveTo(xd1, yd1)
        gameboard.add(drawn[1].image)
    if drawn[2]:
        drawn[2].image.moveTo(xd2, yd2)
        gameboard.add(drawn[2].image)
    if drawn[3]:
        drawn[3].image.moveTo(xd3, yd3)
        gameboard.add(drawn[3].image)


def main():
    # prompt for starting a new game
    print ("Welcome to Heart!\n")

    # create four player
    player0 = Player()
    player1 = Player()
    player2 = Player()
    player3 = Player()

    playerlist = [player0, player1, player2, player3]

    ended = False
    
    # round goes on while someone dead
    while not ended:
        #create a deck
        deck = []
        deck = create_deck()
        drawn = [None, None, None, None]
        
        # start to draw cards
        for i in range(13):
            for player in playerlist:
                card = deck.pop()
                player.suitindex[card.suit] += 1
                player.cards.append(card)

        # sort player's cards
        sorted = False
        
        while not sorted:
            sorted = True
            for i in range(len(player0.cards) - 1):
                if player0.cards[i].code > player0.cards[i + 1].code:
                    player0.cards[i], player0.cards[i + 1] = player0.cards[i + 1], player0.cards[i]
                    sorted = False
            
        update_card(playerlist)
        print(player0.suitindex)

        turn = 0
        reference = 0
        initial = True
        turnstarted = False
        heartbrokne = False

        # play round repeatedely until no one has cards
        while turn != 52:

        # player0 turn
            if initial:
                for card in player0.cards:
                    if card.code == 0:
                        player0.firstturn = True

            if player0.firstturn or turnstarted:
                valid = False
                while not valid:
                    valid = True
                    index = select(playerlist)
                    if not player0.firstturn:
                        if player0.cards[index].suit != reference.suit:
                            if player0.suitindex[reference.suit] != 0:
                                valid = False
                    if turn == 0:
                        if player0.cards[index].code != 0:
                            valid = False
                        
                
                selection = player0.cards.pop(index)
                drawn[0] = selection
                update_card(playerlist, drawn)

                if player0.firstturn:
                    reference = drawn[0]
                        
        # player1 turn
            time.sleep(1)
            if initial:
                for card in player1.cards:
                    if card.code == 0:
                        player1.firstturn = True
            
            if player1.firstturn or turnstarted:
                index = player_AI(playerlist, drawn, 1)
                selection = player1.cards.pop(index)
                drawn[1] = selection
                update_card(playerlist, drawn)

                if player1.firstturn:
                    reference = drawn[1]

        # player2 turn
            time.sleep(1)
            if initial:
                for card in player2.cards:
                    if card.code == 0:
                        player2.firstturn = True
            
            if player2.firstturn or turnstarted:
                index = player_AI(playerlist, drawn, 2)
                selection = player2.cards.pop(index)
                drawn[2] = selection
                update_card(playerlist, drawn)

                if player2.firstturn:
                    reference = drawn[2]

        # player3 turn
            time.sleep(1)
            if initial:
                for card in player3.cards:
                    if card.code == 0:
                        player3.firstturn = True
            
            if player3.firstturn or turnstarted:
                index = player_AI(playerlist, drawn, 3)
                selection = player3.cards.pop(index)
                drawn[3] = selection
                update_card(playerlist, drawn)

                if player3.firstturn:
                    reference = drawn[3]

        # card evaluation
            


#MAIN PROGRAM STARTS HERE

main()
