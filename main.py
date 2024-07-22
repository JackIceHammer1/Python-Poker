import random

# Constants
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6', '7': 7', '8': 8', '9': 9', '10': 10', 'J': 10', 'Q': 10', 'K': 10', 'A': 11}

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
        self.bet = 0
    
    def add_card(self, card):
        self.cards.append(card)
    
    def calculate_value(self):
        value = sum(VALUES[card.rank] for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 'A')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value
    
    def __repr__(self):
        return ', '.join(map(str, self.cards))
    
    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

# PokerGame class
class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hands = [Hand()]
        self.dealer_hand = Hand()
        self.player_blackjack = False
        self.dealer_blackjack = False
        self.player_bankroll = 1000
        self.game_over = False
    
    def deal_initial_cards(self):
        for _ in range(2):
            self.player_hands[0].add_card(self.deck.deal_card())
            self.dealer_hand.add_card(self.deck.deal_card())
        self.check_blackjack()
    
    def check_blackjack(self):
        if self.player_hands[0].calculate_value() == 21:
            self.player_blackjack = True
        if self.dealer_hand.calculate_value() == 21:
            self.dealer_blackjack = True
    
    def show_hands(self, reveal_dealer=False):
        for i, hand in enumerate(self.player_hands):
            print(f'Player\'s Hand {i+1}: {hand} (Value: {hand.calculate_value()})')
        if reveal_dealer:
            print(f'Dealer\'s Hand: {self.dealer_hand} (Value: {self.dealer_hand.calculate_value()})')
        else:
            print(f'Dealer\'s Hand: {self.dealer_hand.cards[0]} and [Hidden]')
    
    def player_turn(self):
        for hand in self.player_hands:
            while not self.game_over:
                action = input("Choose action: (H)it, (S)tand, (D)ouble down, s(P)lit: ").upper()
                if action == 'H':
                    hand.add_card(self.deck.deal_card())
                    print(f'Player\'s Hand: {hand} (Value: {hand.calculate_value()})')
                    if hand.calculate_value() > 21:
                        print("Player busts!")
                        self.game_over = True
                elif action == 'S':
                    break
                elif action == 'D':
                    if len(hand.cards) == 2:
                        hand.add_card(self.deck.deal_card())
                        hand.bet *= 2
                        print(f'Player\'s Hand: {hand} (Value: {hand.calculate_value()})')
                        if hand.calculate_value() > 21:
                            print("Player busts!")
                        break
                elif action == 'P':
                    if hand.can_split():
                        new_hand = Hand()
                        new_hand.add_card(hand.cards.pop())
                        hand.add_card(self.deck.deal_card())
                        new_hand.add_card(self.deck.deal_card())
                        self.player_hands.append(new_hand)
                        self.show_hands()
                    else:
                        print("Cannot split this hand.")
                else:
                    print("Invalid action. Please choose 'H', 'S', 'D', or 'P'.")
    
    def dealer_turn(self):
        while self.dealer_hand.calculate_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
    
    def determine_winner(self):
        if self.player_blackjack and not self.dealer_blackjack:
            self.player_bankroll += self.player_hands[0].bet * 1.5
            return "Player wins with Blackjack!"
        if self.dealer_blackjack and not self.player_blackjack:
            self.player_bankroll -= self.player_hands[0].bet
            return "Dealer wins with Blackjack!"
        
        player_total = sum(hand.calculate_value() for hand in self.player_hands)
        dealer_value = self.dealer_hand.calculate_value()
        
        if player_total > 21:
            self.player_bankroll -= sum(hand.bet for hand in self.player_hands)
            return "Dealer wins!"
        elif dealer_value > 21 or player_total > dealer_value:
            self.player_bankroll += sum(hand.bet for hand in self.player_hands)
            return "Player wins!"
        elif player_total < dealer_value:
            self.player_bankroll -= sum(hand.bet for hand in self.player_hands)
            return "Dealer wins!"
        else:
            return "It's a tie!"
    
    def place_bet(self):
        while True:
            try:
                bet = int(input(f'You have ${self.player_bankroll}. Place your bet: '))
                if 0 < bet <= self.player_bankroll:
                    self.player_hands[0].bet = bet
                    break
                else:
                    print(f'Invalid bet amount. You have ${self.player_bankroll}.')
            except ValueError:
                print('Please enter a valid number.')
    
    def reset_game(self):
        self.player_hands = [Hand()]
        self.dealer_hand = Hand()
        self.player_blackjack = False
        self.dealer_blackjack = False
        self.game_over = False
    
    def play(self):
        while True:
            self.reset_game()
            self.place_bet()
            self.deal_initial_cards()
            self.show_hands()
            
            if not self.player_blackjack and not self.dealer_blackjack:
                self.player_turn()
                if not self.game_over:
                    self.dealer_turn()
                self.show_hands(reveal_dealer=True)
            
            print(self.determine_winner())
            
            if self.player_bankroll <= 0:
                print('You are out of money! Game over.')
                break
            
            play_again = input('Do you want to play another round? (Y/N): ').upper()
            if play_again != 'Y':
                break

# Example usage
if __name__ == "__main__":
    game = PokerGame()
    game.play()
