"""
Assignment 2: Klondike 

Zayd Biberdorf
"""


# custom exceptions


from os import name


class argumentError(Exception):
    "Raised when there is an invalid argument"
    pass


class argumentLengthError(Exception):
    "raised when there is an invalid number of arguments"

    def __init__(self, userInput):
        self.message = "%s: incorrect number of arguments" % (userInput)
        super().__init__(self.message)


class ErrorOpeningFile(Exception):
    "raised when there is an invalid number of arguments"

    def __init__(self, fileName):
        self.message = "%s:  could not open file" % (fileName)
        super().__init__(self.message)


class formatFileError(Exception):
    "raised when there is a format error in a file"

    def __init__(self, fileName):
        self.message = "%s: format error in file" % (fileName)
        super().__init__(self.message)


class incorrectArgumentsError(Exception):
    def __init__(self, argument):
        self.message = "%s: arguments incorrect" % (argument)
        super().__init__(self.message)


class invalidMoveError(Exception):
    "raised when there is an invalid number of arguments"

    def __init__(self, userInput):
        self.message = "%s: illegal move" % (userInput)

        super().__init__(self.message)


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.isVisible = False

    def __str__(self):
        cardString = self.rank + self.suit
        return cardString

    def __repr__(self):

        if self.isVisible:
            return self.rank + self.suit + "+"
        else:
            return self.rank + self.suit + "-"

    def isvisibleCard(self):
        return self.isVisible

    def faceupCard(self, visible):
        self.isVisible = visible

    def rankCard(self):
        return self.rank

    def suitCard(self):
        return self.suit


class Deck:
    def __init__(self, name):
        self.name = name
        self.pile = []

    def __str__(self):
        """
        Return a printable stiring representation of the deck
        input: N/A
        output: N/A
        """

        pileString = "["

        for item in reversed(self.pile):
            pileString += " "
            if item.isvisibleCard():
                pileString += str(item)
            else:
                pileString += "??"

        pileString += " ]"
        deckName = self.name
        while len(deckName) < 8:
            deckName = " " + deckName

        return "%s %s" % (deckName, pileString)

    def __repr__(self):
        """
        this will make sure each card has a '+' or '-' to represent if it is showing or not
        """
        deckName = self.name
        while len(deckName) < 8:
            deckName = " " + deckName

        cheatString = deckName + " ["

        for item in reversed(self.pile):
            cheatString += " "
            if item not in ["[", "]"]:
                cheatString += str(item.__repr__())
            else:
                cheatString += item
        cheatString += " ]"

        return cheatString

    def nameDeck(self):
        return self.name

    def sizeDeck(self):
        return len(self.pile)

    def isEmptyDeck(self):
        if self.sizeDeck() == 0:
            return True
        else:
            return False

    def pushDeck(self, card):
        self.pile.append(card)

    def popDeck(self):
        return self.pile.pop()

    def peekDeck(self):
        return self.pile[len(self.pile) - 1]


def loadGame(fileName):
    """
    this function will load a game from a text file turning it into decks fi8lled with cards
    input: fileName [str]
    output: piles [list]
    """
    piles = []
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    assert len(lines) == 13, formatFileError(fileName)
    for line in lines:
        items = line.split()
        deckName = Deck(items.pop(0))
        for item in reversed(items):
            if item not in ["[", "]"]:
                newCard = Card(item[1], item[0])
                if item[2] == "+":
                    newCard.faceupCard(True)
                deckName.pushDeck(newCard)

        piles.append(deckName)

    return piles


def saveGame(decks, fileName):
    """
    this function will convert the current game state into a text file for it to be saved
    input: decks [list], fileName  [str]
    output: N/A
    """
    file = open(fileName, "w")
    count = 0
    for deck in decks:
        count += 1
        if count < len(decks):
            file.writelines("%s \n" % (deck.__repr__()))
        else:
            file.writelines("%s" % (deck.__repr__()))

    file.close()


def isValidMove(moveTo, moveFrom, userInput, decks):
    """
    This function will determine wether or not the move is valid
    input: userInput [list], decks[list]
    output: (moveTo, moveFrom) [tuple]
    """

    assert (
        moveFrom.sizeDeck() > 0 and userInput[0].lower() != "stock"
    ), invalidMoveError(userInput)

    if moveTo.nameDeck() in ["Spades", "Hearts", "Diamonds", "Clubs"]:
        if moveTo.isEmptyDeck() == True:
            if moveFrom.peekDeck().rankCard() != "A":
                raise invalidMoveError(userInput)
        else:
            if (
                moveTo.peekDeck().rankCard() not in ["K", "Q", "J", "A", "2", "T"]
            ) and (
                (moveFrom.peekDeck().rankCard() not in ["K", "Q", "J", "A", "2", "T"])
            ):
                if (
                    int(moveFrom.peekDeck().rankCard())
                    != int(moveTo.peekDeck().rankCard()) + 1
                ):
                    raise invalidMoveError(userInput)

            else:
                if (
                    moveTo.peekDeck().rankCard() == "A"
                    and moveFrom.peekDeck().rankCard() != "2"
                ):
                    raise invalidMoveError(userInput)
                elif (
                    moveTo.peekDeck().rankCard() == "2"
                    and moveFrom.peekDeck().rankCard() != "3"
                ):
                    raise invalidMoveError(userInput)
                elif (
                    moveTo.peekDeck().rankCard() == "9"
                    and moveFrom.peekDeck().rankCard() != "T"
                ):
                    raise invalidMoveError(userInput)
                elif (
                    moveTo.peekDeck().rankCard() == "J"
                    and moveFrom.peekDeck().rankCard() != "Q"
                ):
                    raise invalidMoveError(userInput)
                elif (
                    moveTo.peekDeck().rankCard() == "Q"
                    and moveFrom.peekDeck().rankCard() != "K"
                ):
                    raise invalidMoveError(userInput)
                elif moveTo.peekDeck().rankCard() == "K":
                    raise invalidMoveError(userInput)

    elif moveTo.isEmptyDeck() == True:
        if moveFrom.peekDeck().rankCard() != "K":
            raise invalidMoveError(userInput)
    else:
        if (moveTo.peekDeck().rankCard() not in ["K", "Q", "J", "A", "2", "T"]) and (
            (moveFrom.peekDeck().rankCard() not in ["K", "Q", "J", "A", "2", "T"])
        ):
            if (
                int(moveFrom.peekDeck().rankCard())
                != int(moveTo.peekDeck().rankCard()) - 1
            ):
                raise invalidMoveError(userInput)

        else:
            if (
                moveTo.peekDeck().rankCard() == "K"
                and moveFrom.peekDeck().rankCard() != "Q"
            ):
                raise invalidMoveError(userInput)
            elif (
                moveTo.peekDeck().rankCard() == "Q"
                and moveFrom.peekDeck().rankCard() != "J"
            ):
                raise invalidMoveError(userInput)
            elif (
                moveTo.peekDeck().rankCard() == "J"
                and moveFrom.peekDeck().rankCard() != "T"
            ):
                raise invalidMoveError(userInput)
            elif (
                moveTo.peekDeck().rankCard() == "T"
                and moveFrom.peekDeck().rankCard() != "9"
            ):
                raise invalidMoveError(userInput)

            elif (
                moveTo.peekDeck().rankCard() == "2"
                and moveFrom.peekDeck().rankCard() != "A"
            ):
                raise invalidMoveError(userInput)
            elif (
                moveTo.peekDeck().rankCard() == "A"
                or moveFrom.peekDeck().rankCard() == "K"
            ):
                raise invalidMoveError(userInput)


def discard(decks):
    """
    this functoin will move 3 card from the stock pile (or less depending on if there are enough cards in stock)
    input: decks [list]
    output: N/A
    """
    if decks[0].sizeDeck() >= 3:
        for i in range(3):
            item = decks[0].popDeck()
            item.faceupCard(False)
            decks[1].pushDeck(item)
            if decks[0].sizeDeck() > 0:
                decks[0].peekDeck().faceupCard(True)
    else:
        for i in range(decks[0].sizeDeck()):
            item = decks[0].popDeck()
            item.faceupCard(False)
            decks[1].pushDeck(item)
            if decks[0].sizeDeck() > 0:
                decks[0].peekDeck().faceupCard(True)


def reset(decks):
    """
    Move the Discard cards into Stock, leaving Discard empty. The
    Stock cards are in the order in which they were discarded. The top Stock card is turned face-up.
    input: decks [list]
    output: N/A
    """

    cards = []
    while decks[1].sizeDeck() > 0:
        cards.append(decks[1].popDeck())

    for card in reversed(cards):
        decks[0].pushDeck(card)

    decks[0].peekDeck().faceupCard(True)


def move(userInput, decks):
    """
    This function will move cards from one place to another if the move is valid
    input: user input [list], decks
    output: N/A
    """
    assert len(userInput) == 3, incorrectArgumentsError(userInput)
    previousCards = []
    validMove = [False, False]
    for deck in decks:
        if userInput[1] in deck.nameDeck().lower():
            moveFrom = deck
            validMove[0] = True
        if userInput[2] in deck.nameDeck().lower():
            moveTo = deck
            validMove[1] = True

    assert moveFrom.sizeDeck() > 0, invalidMoveError(userInput)

    if userInput[2].lower() == "suit":
        for suitDeck in [decks[2], decks[3], decks[4], decks[5]]:
            nameDeck = suitDeck.nameDeck()
            if moveFrom.peekDeck().suitCard() == nameDeck[0].lower():
                moveTo = suitDeck
                validMove[1] = True

    if False in validMove:
        raise invalidMoveError(userInput)

    assert "stock" not in moveTo.nameDeck().lower(), invalidMoveError(userInput)

    try:
        isValidMove(moveTo, moveFrom, userInput, decks)
    except invalidMoveError:
        previousCards.append(moveFrom.popDeck())
        while previousCards[-1].isvisibleCard():
            try:
                if moveFrom.sizeDeck() > 0 and moveTo.sizeDeck() > 0:
                    isValidMove(moveTo, moveFrom, userInput, decks)
                else:
                    raise invalidMoveError(userInput)
            except invalidMoveError:
                pass
            else:
                if moveFrom.peekDeck().isvisibleCard():
                    itemToMove = moveFrom.popDeck()
                    moveTo.pushDeck(itemToMove)
                    for card in previousCards:
                        if card.suitCard() != moveTo.nameDeck()[0].lower():
                            raise invalidMoveError(userInput)

                    if len(previousCards) != 0:
                        for card in reversed(previousCards):
                            moveTo.pushDeck(card)
                    if moveFrom.sizeDeck() > 0:
                        moveFrom.peekDeck().faceupCard(True)
                    return print("Executing: %s" % (userInput))
            if moveFrom.sizeDeck() > 0 and moveTo.sizeDeck() > 0:
                previousCards.append(moveFrom.popDeck())
            else:
                for card in reversed(previousCards):
                    moveFrom.pushDeck(card)
                raise invalidMoveError(userInput)
    else:
        itemToMove = moveFrom.popDeck()
        moveTo.pushDeck(itemToMove)
        if len(previousCards) != 0:
            for card in previousCards:
                moveTo.pushDeck(card)
        if moveFrom.sizeDeck() > 0:
            moveFrom.peekDeck().faceupCard(True)
        return print("Executing: %s" % (userInput))

    for card in reversed(previousCards):
        moveFrom.pushDeck(card)
    raise invalidMoveError(userInput)


def main():
    """
    the main function is used to handle user unput and call fuctions acoordingly, also used to handle exeptions
    input: N/A
    output: N/A
    """
    quit = False
    decks = []
    print("Welcome to Klondike!")
    while not quit:
        userInput = input("Your Move: ")
        userInput = userInput.split()
        try:
            if "load" in userInput:
                if len(userInput) > 2 or len(userInput) < 2:
                    raise incorrectArgumentsError(userInput)
                elif userInput[1][-4:] != ".txt":
                    raise ErrorOpeningFile(userInput[1])
                else:
                    decks = loadGame(userInput[1])
                    print("Executing: %s" % (userInput))
            elif "board" in userInput:
                if len(userInput) != 1:
                    raise incorrectArgumentsError(userInput)
                else:
                    print("Executing: %s" % (userInput))
                    print("Klondike!")
                    for pile in decks:
                        print(pile)
            elif "cheat" in userInput:
                if len(userInput) != 1:
                    raise incorrectArgumentsError(userInput)
                else:
                    for deck in decks:
                        print(deck.__repr__())
            elif "done" in userInput:
                quit = True
                if len(userInput) != 1:
                    raise incorrectArgumentsError(userInput)
                else:
                    print("Executing: %s" % (userInput))
            elif "comment" in userInput:
                if len(userInput) > 3 or len(userInput) < 3:
                    raise incorrectArgumentsError(userInput)
                else:
                    print("%s: %s %s" % (userInput[0], userInput[1], userInput[2]))
            elif "move" in userInput:
                exicuteMessage = move(userInput, decks)
                if exicuteMessage != None:
                    print(exicuteMessage)
            elif "discard" in userInput:
                if decks[0].sizeDeck() == 0:
                    raise invalidMoveError(userInput)
                else:
                    discard(decks)
                    print("Executing: %s" % (userInput))
            elif "reset" in userInput:
                if len(userInput) == 1 and decks[0].sizeDeck() == 0:
                    reset(decks)
                    print("Executing: %s" % (userInput))
                else:
                    raise incorrectArgumentsError(userInput)
            elif "save" in userInput:
                if len(userInput) == 2:
                    saveGame(decks, userInput[1])
                    print("Executing: %s" % (userInput))
                else:
                    raise incorrectArgumentsError(userInput)
            else:
                raise incorrectArgumentsError(userInput)

            gameWon = True
            for deck in decks:
                if (
                    deck.nameDeck() in ["Spades", "Hearts", "Diamonds", "Clubs"]
                    and deck.sizeDeck() != 13
                ):
                    gameWon = False
            if gameWon == True:
                print("Congratulations!!!!")

        except AssertionError as error:
            print(error)
        except argumentError:
            print("%s: arguments incorrect" % (userInput))
        except argumentLengthError as error:
            print(error)
        except formatFileError as error:
            print(error)
        except ErrorOpeningFile as error:
            print(error)
        except incorrectArgumentsError as error:
            print(error)
        except invalidMoveError as error:
            print(error)


main()
