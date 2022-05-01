import random
import time
from cs1graphics import *

img_path = './images/'

suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
face_names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
value = [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]



gameboard = Canvas(600, 400, 'dark green', 'One Card')


"""
Define the Card class
"""
class Card:
    """Information for card"""
    pass


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
            card.suit = suit_names[i]
            card.value = value[j]
            card.image = img
            card.state = True
            card.pick = 0
            deck.append(card)

    for i in range(2):    
        img = Image('./cards/joker' + str(i) + '.png')
        card = Card()
        card.face = 'Joker'
        card.suit = 'Joker'
        card.value = 7
        card.image = img
        card.state = True
        card.pick = 0
        deck.append(card)
    
    random.shuffle(deck)

    return deck

def reshuffle(deck, drawn):
    ResultA = []
    ResultB = []

    ResultB.append(drawn.pop())
    for cards in drawn:
        ResultA.append(cards)
    random.shuffle(ResultA)
    print('Reshuffle cards...')
    
    return ResultA, ResultB


def suitchange(dealer, player, drawn):
       suitlist = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
       index = suitlist.index(drawn.suit)

       cardlist = []
       for i in range(4):
           img = Image('./cards/' + suitlist[i] + '_' + '7' + '.png')
           seven_card = Card()
           seven_card.suit = suitlist[i]
           seven_card.face = '7'
           seven_card.image = img
           seven_card.state = True
           cardlist.append(seven_card)
           

       while True:
        wait = gameboard.wait()
        keytype = wait.getDescription()
        if keytype == 'keyboard':
            keyinput = wait.getKey()
            if keyinput == 'a':
                if index == 0:
                    index = len(suitlist) - 1
                else:
                    index -= 1

                cards = cardlist[index]
                update_card(dealer, player, cards, ('seven', None))
            elif keyinput == 'd':
                if index == len(suitlist) - 1:
                    index = 0
                else:
                    index += 1

                cards = cardlist[index]
                update_card(dealer, player, cards, ('seven', None))
            elif keyinput == 'w':
                return cards
    

def select(dealer, player, drawn, message = (None, None)):
    """
    Select card player want to draw by moving arrow.
    If there's no card to draw, just take card from deck by press spacebar.
    """
    index = 0
    player[0].pick = 20
    update_card(dealer, player, drawn, message)
    
    while True:
        wait = gameboard.wait()
        keytype = wait.getDescription()
        if keytype == 'keyboard':
            keyinput = wait.getKey()
            if keyinput == 'a':
                if index == 0:
                    player[index].pick = 0
                    index = len(player) - 1
                    player[index].pick = 20
                else:
                    player[index].pick = 0
                    index -= 1
                    player[index].pick = 20
                
                update_card(dealer, player, drawn, message)
            elif keyinput == 'd':
                if index == len(player) - 1:
                    player[index].pick = 0
                    index = 0
                    player[index].pick = 20
                else:
                    player[index].pick = 0
                    index += 1
                    player[index].pick = 20
                
                update_card(dealer, player, drawn, message)
            elif keyinput == 'w':
                player[index].pick = 0
                return index
            elif keyinput == 'x':
                player[index].pick = 0
                return 'draw'
                

    user_decision = input(prompt)
        
    if user_decision == 'draw':
        return 'draw'

    return int(user_decision) - 1


def dealer_AI(dealer, drawn, attack):
    """
    Select optimal card to draw
    If there's no card to draw, it returns None.
    """
    if attack != 0:
        for index in range(len(dealer)):
            card = dealer[index]
            if card.face == drawn.face and card.value >= drawn.value:
                return index
        
        for index in range(len(dealer)):
            card = dealer[index]
            if card.suit == drawn.suit and card.value >= drawn.value:
                return index

        for index in range(len(dealer)):
            card = dealer[index]
            if card.suit == 'Joker':
                return index
        
        return None

    if drawn.suit == 'Joker':
        print('fuck you!')
        index = random.randint(0, len(dealer) - 1)
        return index
    
    for index in range(len(dealer)):
        card = dealer[index]
        if card.face == drawn.face:
            return index
    
    for index in range(len(dealer)):
        card = dealer[index]
        if card.suit == drawn.suit:
            return index

    for index in range(len(dealer)):
        card = dealer[index]
        if card.suit == 'Joker':
            return index

    return None


def update_card(dealer, player, drawn = None, message = (None, None)):
    """
    Update card drawn on the canvas.
    message : (<type of message>, <additional information>)
    """
    depth = 100
    x0, y0 = 100,400
    x1, y1 = 100,0
    x2, y2 = 200, 200
    x3, y3 = 300, 200

    gameboard.clear()
    
    delta = 0
    
    for cards in player:
        cards.image.moveTo(x0 + delta, y0 - cards.pick)
        gameboard.add(cards.image)
        delta += 15
    num_player = Text(str(len(player)), 16)
    num_player.setFontColor('Yellow')
    num_player.moveTo(15, 380)
    gameboard.add(num_player)

    if len(player) == 1:
        onecard = Text('ONE CARD!!', 16)
        onecard.setFontColor('Red')
        onecard.moveTo(300, 380)
        gameboard.add(onecard)
    
    delta = 0
    
    for cards in dealer:
        Back = Image('./cards/Back.png')
        Back.moveTo(x1 + delta, y1)
        gameboard.add(Back)
        delta += 15
    num_dealer = Text(str(len(dealer)), 16)
    num_dealer.setFontColor('Yellow')
    num_dealer.moveTo(15, 20)
    gameboard.add(num_dealer)

    if len(dealer) == 1:
        onecard = Text('ONE CARD!!', 16)
        onecard.setFontColor('Red')
        onecard.moveTo(300, 20)
        gameboard.add(onecard)

    Back = Image('./cards/Back.png')
    Back.moveTo(x2, y2)
    gameboard.add(Back)
    
    if drawn == None:
            return

    drawn.image.moveTo(x3, y3)
    gameboard.add(drawn.image)

    if message[0]:
        msgtype, msginfo = message

        if msgtype == 'attack':
            msg = 'Attack!! Stack is %d'%msginfo
            text = Text(msg, 16)
            text.setFontColor('Red')
            text.moveTo(450, 200)
            gameboard.add(text)
            time.sleep(0.5)
        elif msgtype == 'seven':
            msg = 'Change Suit of Card!'
            text = Text(msg, 16)
            text.setFontColor('Yellow')
            text.moveTo(450, 200)
            gameboard.add(text)
        elif msgtype == 'end':
            if msginfo == 'player':
                msg = 'PLAYER WON THE GAME!!!'
                text = Text(msg, 20)
                text.setFontColor('Yellow')
                text.moveTo(300, 300)
                gameboard.add(text)
            elif msginfo == 'dealer':
                msg = 'DEALER WON THE GAME!!!'
                text = Text(msg, 20)
                text.setFontColor('Yellow')
                text.moveTo(300, 300)
                gameboard.add(text)
        elif msgtype == 'bankrupt':
            if msginfo == 'player':
                msg = 'PLAYER BANKRUPTED!!!'
                text = Text(msg, 20)
                text.setFontColor('Red')
                text.moveTo(300, 300)
                gameboard.add(text)
            elif msginfo == 'dealer':
                msg = 'DEALER BANKRUPTED!!!'
                text = Text(msg, 20)
                text.setFontColor('Red')
                text.moveTo(300, 300)
                gameboard.add(text)

def main():

    deck = []

    # prompt for starting a new game and create a deck
    print ("Welcome to One Card!\n")
    if len(deck) < 12:
        deck = create_deck()

    # create two hands of dealer and player
    dealer = []
    player = []
    drawn = []
    attack = 0
    seven = False

    # start to draw seven cards
    for i in range(7):
        card = deck.pop()
        player.append(card)

    for i in range(7):
        card = deck.pop()
        card.state = False
        dealer.append(card)

    drawn.append(deck.pop())

    update_card(dealer, player, drawn[-1])


    # play one card repeatedely
    while True:

    # player's turn
        turn_ended = False
        
        while not turn_ended:
            message = (None, None)
            if attack != 0:
                message = ('attack', attack)
            selection = select(dealer, player, drawn[-1], message)

            if selection == 'draw':
                if attack == 0:
                    attack = 1
                    
                for i in range(attack):
                    if len(deck) == 0:
                        deck, drawn = reshuffle(deck, drawn)
                    card = deck.pop()
                    player.append(card)
                    update_card(dealer, player, drawn[-1])
                    time.sleep(0.5)
                    
                attack = 0
                turn_ended = True
                
            else:
                selected = player[selection]
                
                if selected.suit == drawn[-1].suit or selected.face == drawn[-1].face or drawn[-1].suit == 'Joker' or selected.suit == 'Joker':
                    if attack == 0 or attack != 0 and selected.value >= drawn[-1].value:
                        player.pop(selection)
                        if seven:
                            drawn.pop()
                            seven = False
                        drawn.append(selected)
                        update_card(dealer, player, drawn[-1])

                        if not drawn[-1].face in ['Jack', 'King']:
                            turn_ended = True
                        
                        if len(player) == 0:
                            turn_ended = True

                        if drawn[-1].value != 0:
                            attack += drawn[-1].value
                            update_card(dealer, player, drawn[-1], ('attack', attack))

                        if drawn[-1].face == '7':
                            update_card(dealer, player, drawn[-1], ('seven', None))
                            changed_card = suitchange(dealer, player, drawn[-1])
                            drawn.append(changed_card)
                            seven = True
                            update_card(dealer, player, drawn[-1])
                    
            
    # player statecheck
        if len(player) > 20:
            update_card(dealer, player, drawn[-1], ('bankrupt', 'player'))
            return
        if len(player) == 0:
            update_card(dealer, player, drawn[-1], ('end', 'player'))
            return

        
    # dealer's turn
        time.sleep(1)
        turn_ended = False
        
        while not turn_ended:
            index = dealer_AI(dealer, drawn[-1], attack)

            if index == None:
                if attack == 0:
                    attack = 1
                    
                for i in range(attack):
                    if len(deck) == 0:
                        deck, drawn = reshuffle(deck, drawn)
                    card = deck.pop()
                    dealer.append(card)
                    update_card(dealer, player, drawn[-1])
                    time.sleep(0.5)

                attack = 0
                turn_ended = True
                
            else:
                card = dealer[index]
                
                dealer.pop(index)
                if seven:
                    drawn.pop()
                    seven = False
                drawn.append(card)
                update_card(dealer, player, drawn[-1])

                if not drawn[-1].face in ['Jack', 'King']:
                    turn_ended = True
                
                if len(dealer) == 0:
                    turn_ended = True
                
                if drawn[-1].value != 0:
                    attack += drawn[-1].value
                    update_card(dealer, player, drawn[-1], ('attack', attack))

            time.sleep(1)

    #dealer statecheck
        if len(dealer) > 20:
            update_card(dealer, player, drawn[-1], ('bankrupt', 'dealer'))
            return
        if len(dealer) == 0:
            update_card(dealer, player, drawn[-1], ('end', 'dealer'))
            return

main()
