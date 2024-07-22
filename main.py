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
                action = input(f"Choose action for Hand {self.player_hands.index(hand) + 1}: (H)it, (S)tand, (D)ouble down, s(P)lit: ").upper()
                if action == 'H':
                    hand.add_card(self.deck.deal_card())
                    print(f'Player\'s Hand {self.player_hands.index(hand) + 1}: {hand} (Value: {hand.calculate_value()})')
                    if hand.calculate_value() > 21:
                        print("Player busts!")
                        self.game_over = True
                elif action == 'S':
                    break
                elif action == 'D':
                    if len(hand.cards) == 2:
                        hand.add_card(self.deck.deal_card())
                        hand.bet *= 2
                        print(f'Player\'s Hand {self.player_hands.index(hand) + 1}: {hand} (Value: {hand.calculate_value()})')
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
                        print(f"Hands split! New Hand {len(self.player_hands)} added.")
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
        
        results = []
        dealer_value = self.dealer_hand.calculate_value()
        
        for i, hand in enumerate(self.player_hands):
            player_total = hand.calculate_value()
            if player_total > 21:
                results.append(f'Player Hand {i+1} busts!')
                self.player_bankroll -= hand.bet
            elif dealer_value > 21 or player_total > dealer_value:
                results.append(f'Player Hand {i+1} wins!')
                self.player_bankroll += hand.bet
            elif player_total < dealer_value:
                results.append(f'Dealer wins against Player Hand {i+1}!')
                self.player_bankroll -= hand.bet
            else:
                results.append(f'Player Hand {i+1} ties with Dealer.')
        
        return '\n'.join(results)
    
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
    
    def offer_insurance(self):
        if self.dealer_hand.cards[0].rank == 'A':
            while True:
                insurance_bet = input("Dealer shows an Ace. Do you want to take insurance? (Y/N): ").upper()
                if insurance_bet == 'Y':
                    insurance = self.player_hands[0].bet / 2
                    if self.dealer_blackjack:
                        self.player_bankroll += insurance
                        print("Dealer has Blackjack! Insurance pays 2:1.")
                    else:
                        self.player_bankroll -= insurance
                        print("Dealer does not have Blackjack. Insurance lost.")
                    break
                elif insurance_bet == 'N':
                    break
                else:
                    print("Invalid input. Please choose 'Y' or 'N'.")
    
    def split_hands(self):
        if self.player_hands[0].can_split():
            hand1 = Hand()
            hand2 = Hand()
            hand1.add_card(self.player_hands[0].cards[0])
            hand2.add_card(self.player_hands[0].cards[1])
            self.player_hands = [hand1, hand2]
            for hand in self.player_hands:
                hand.add_card(self.deck.deal_card())
            print(f"Hands split! New Hand {len(self.player_hands)} added.")
            self.show_hands()

    def additional_betting_rounds(self):
        for i, hand in enumerate(self.player_hands):
            if not self.game_over:
                while True:
                    bet = input(f"Do you want to place an additional bet on Hand {i+1}? (Y/N): ").upper()
                    if bet == 'Y':
                        additional_bet = int(input(f"Place additional bet for Hand {i+1}: "))
                        hand.bet += additional_bet
                        break
                    elif bet == 'N':
                        break
                    else:
                        print("Invalid input. Please choose 'Y' or 'N'.")

    def advanced_dealer_logic(self):
        dealer_value = self.dealer_hand.calculate_value()
        if dealer_value < 17:
            print("Dealer has less than 17. Drawing more cards.")
            while dealer_value < 17:
                self.dealer_hand.add_card(self.deck.deal_card())
                dealer_value = self.dealer_hand.calculate_value()
                print(f'Dealer\'s Hand: {self.dealer_hand} (Value: {dealer_value})')
        elif dealer_value == 17:
            if any(card.rank == 'A' for card in self.dealer_hand.cards):
                print("Dealer has a soft 17 (includes an Ace). Drawing more cards.")
                while dealer_value < 18:
                    self.dealer_hand.add_card(self.deck.deal_card())
                    dealer_value = self.dealer_hand.calculate_value()
                    print(f'Dealer\'s Hand: {self.dealer_hand} (Value: {dealer_value})')

# Example usage
if __name__ == "__main__":
    game = PokerGame()
    game.play()
