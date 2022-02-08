import random

# Defining my main function


def main():
    # creating the deck,
    # shuffling the deck,
    # creating the player and filling his hand with 5 card then displaying the cards in his hand aloong side the rest of the cards in the deck then asking for which color the user would like to take the sum of.
    deck = Deck()
    deck.shuffle()
    player = Player()
    for index in range(0, 5):
        player.add(deck.deal())
    player.display()
    deck.display()
    input_color = input("Select a color (R, G, B, Y):")
    print(
        "The sum of",
        input_color.upper(),
        "cards in the player's hand is:",
        player.colored_cards(input_color),
    )


# Creating the card class


class Card:
    def __init__(self, rank, color):
        # The card class will have the following properties:
        #       - rank of the card ranging from 1-4
        #       - the color of the card will be R, B, Y, G
        #       - finaly we put them together to create the card
        self.rank = rank
        self.color = color
        self.card = str(rank) + color

    # this function will retrun the rank of a card

    def get_rank(self):
        return self.rank

    # this functin will retrun the color of the card

    def get_color(self):
        return self.color

    # this funciton will retrun the full card including the rank and the color

    def display(self):
        return self.card


# creating the deck class


class Deck:
    def __init__(self):
        # this class will the following properites:
        #       - a range of colors
        #       - a list definig the deck holding 16 cards in it, each color will have a rank 1-4
        self.colors = ["R", "B", "Y", "G"]
        self.deck = []

        # This will be an agrorith that will run through each color filling the list with the deck of 16 cards
        for index in range(1, 5):
            i = 0
            for num in range(1, 5):
                name = Card(index, self.colors[i])
                self.deck.append(name.display())
                i += 1

    # this funciton will shuffle the deck putting each card in a random order

    def shuffle(self):
        # Creating the index for the shuffle algorithm
        self.deck_index = len(self.deck) - 1
        # this determines how many times the algorim will run 9 i use a random amount
        for rand_num in range(0, random.randint(50, 100)):
            # chose two random cards from the deck and swap them
            self.card_one_index = random.randrange(0, self.deck_index)
            self.card_two_index = random.randrange(0, self.deck_index)
            self.deck[self.card_one_index], self.deck[self.card_two_index] = (
                self.deck[self.card_two_index],
                self.deck[self.card_one_index],
            )

    # this function will deal a card from the deck retruning the top card an taking that card out of the deck

    def deal(self):
        # saving the "top" card in the deck
        self.top_card = self.deck[0]
        # Removing the top card in the deck
        self.deck.pop()
        # Returnin the top card
        return self.top_card

    # this function will deisplay the cards in the deck
    def display(self):
        # here we loop through all the cards in the deck printing each one
        print("This is the rest of your deck")
        for card in self.deck:
            print("|" + card + "|")


# creatin the player class


class Player:
    def __init__(self):
        # this class will have the following properties:
        #       - the players hand - originally an empty list
        self.players_hand = []

    # this function will add a card to the players hand
    def add(self, card):
        # we add a card by pushing the argument to the list
        self.players_hand.append(card)

    # this funtion will sum up all the cards in a given collor
    def colored_cards(self, color):
        sum_color = 0
        # here we are just checking to see if the collor matches the inputed color and then looping through it adding the rank if they do match then returning the sum
        for card in self.players_hand:
            if card[1] == color.upper():
                sum_color += int(card[0])
        return sum_color

    # this function will display the players hand
    def display(self):
        # here we just loop though the players hand printing each card
        print("This is the players hand")
        for card in self.players_hand:
            print("|" + card + "|")


# this is the game loop
game = True
while game:
    game = False
    # calling the main funciton
    main()
    play_again = input("would you like to play again? (Y/N)")
    if play_again.lower() == "y":
        game = True
