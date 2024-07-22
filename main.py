import random

# Constants
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        return f'{self.rank} of {self.suit}'

# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop()

# Hand class
class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def calculate_value(self):
        value = sum(VALUES[card.rank] for card in self.cards)
        # Adjust for Aces
        num_aces = sum(1 for card in self.cards if card.rank == 'A')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value
    
    def __repr__(self):
        return ', '.join(map(str, self.cards))

# Game class
class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
    
    def deal_initial_cards(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal_card())
            self.dealer_hand.add_card(self.deck.deal_card())
    
    def show_hands(self, reveal_dealer=False):
        print(f'Player\'s Hand: {self.player_hand} (Value: {self.player_hand.calculate_value()})')
        if reveal_dealer:
            print(f'Dealer\'s Hand: {self.dealer_hand} (Value: {self.dealer_hand.calculate_value()})')
        else:
            print(f'Dealer\'s Hand: {self.dealer_hand.cards[0]} and [Hidden]')

# Example usage
if __name__ == "__main__":
    game = PokerGame()
    game.deal_initial_cards()
    game.show_hands()
