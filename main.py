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

# Player class
class Player:
    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = bankroll
        self.hands = [Hand()]
    
    def place_bet(self):
        while True:
            try:
                bet = int(input(f'{self.name}, you have ${self.bankroll}. Place your bet: '))
                if 0 < bet <= self.bankroll:
                    self.hands[0].bet = bet
                    break
                else:
                    print(f'Invalid bet amount. You have ${self.bankroll}.')
            except ValueError:
                print('Please enter a valid number.')
    
    def reset_hands(self):
        self.hands = [Hand()]
    
    def update_bankroll(self, amount):
        self.bankroll += amount
    
    def split_hand(self, hand_index):
        hand = self.hands[hand_index]
        if hand.can_split():
            new_hand = Hand()
            new_hand.add_card(hand.cards.pop())
            hand.add_card(self.deck.deal_card())
            new_hand.add_card(self.deck.deal_card())
            self.hands.append(new_hand)
            print(f"{self.name}'s Hands split! New Hand {len(self.hands)} added.")
            return True
        return False

    def draw_hand(self, hand_index):
        hand = self.hands[hand_index]
        hand.add_card(self.deck.deal_card())

# PokerGame class
class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.dealer_hand = Hand()
        self.dealer_blackjack = False
        self.game_over = False
    
    def add_player(self, name, bankroll):
        self.players.append(Player(name, bankroll))
    
    def deal_initial_cards(self):
        for _ in range(2):
            for player in self.players:
                for hand in player.hands:
                    hand.add_card(self.deck.deal_card())
            self.dealer_hand.add_card(self.deck.deal_card())
        self.check_blackjack()
    
    def check_blackjack(self):
        if self.dealer_hand.calculate_value() == 21:
            self.dealer_blackjack = True
    
    def show_hands(self, reveal_dealer=False):
        for player in self.players:
            for i, hand in enumerate(player.hands):
                print(f'{player.name}\'s Hand {i+1}: {hand} (Value: {hand.calculate_value()})')
        if reveal_dealer:
            print(f'Dealer\'s Hand: {self.dealer_hand} (Value: {self.dealer_hand.calculate_value()})')
        else:
            print(f'Dealer\'s Hand: {self.dealer_hand.cards[0]} and [Hidden]')
    
    def player_turn(self):
        for player in self.players:
            for i, hand in enumerate(player.hands):
                while not self.game_over:
                    action = input(f"{player.name}, choose action for Hand {i+1}: (H)it, (S)tand, (D)ouble down, s(P)lit: ").upper()
                    if action == 'H':
                        player.draw_hand(i)
                        print(f'{player.name}\'s Hand {i+1}: {hand} (Value: {hand.calculate_value()})')
                        if hand.calculate_value() > 21:
                            print(f"{player.name} busts!")
                            break
                    elif action == 'S':
                        break
                    elif action == 'D':
                        if len(hand.cards) == 2:
                            player.draw_hand(i)
                            hand.bet *= 2
                            print(f'{player.name}\'s Hand {i+1}: {hand} (Value: {hand.calculate_value()})')
                            if hand.calculate_value() > 21:
                                print(f"{player.name} busts!")
                            break
                    elif action == 'P':
                        if player.split_hand(i):
                            self.show_hands()
                        else:
                            print("Cannot split this hand.")
                    else:
                        print("Invalid action. Please choose 'H', 'S', 'D', or 'P'.")
    
    def dealer_turn(self):
        while self.dealer_hand.calculate_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
    
    def determine_winner(self):
        if self.dealer_blackjack:
            return "Dealer has Blackjack! All players lose."
        
        results = []
        dealer_value = self.dealer_hand.calculate_value()
        
        for player in self.players:
            for i, hand in enumerate(player.hands):
                player_total = hand.calculate_value()
                if player_total > 21:
                    results.append(f'{player.name} Hand {i+1} busts!')
                    player.update_bankroll(-hand.bet)
                elif dealer_value > 21 or player_total > dealer_value:
                    results.append(f'{player.name} Hand {i+1} wins!')
                    player.update_bankroll(hand.bet)
                elif player_total < dealer_value:
                    results.append(f'Dealer wins against {player.name} Hand {i+1}!')
                    player.update_bankroll(-hand.bet)
                else:
                    results.append(f'{player.name} Hand {i+1} ties with Dealer.')
        
        return '\n'.join(results)
    
    def reset_game(self):
        self.deck = Deck()
        self.dealer_hand = Hand()
        self.dealer_blackjack = False
        self.game_over = False
        for player in self.players:
            player.reset_hands()
    
    def play(self):
        while True:
            self.reset_game()
            for player in self.players:
                player.place_bet()
            self.deal_initial_cards()
            self.show_hands()
            
            if not self.dealer_blackjack:
                self.player_turn()
                if not self.game_over:
                    self.dealer_turn()
                self.show_hands(reveal_dealer=True)
            
            print(self.determine_winner())
            
            for player in self.players:
                if player.bankroll <= 0:
                    print(f'{player.name} is out of money! Removing from game.')
                    self.players.remove(player)
            
            if len(self.players) == 0:
                print('No more players left. Game over.')
                break
            
            play_again = input('Do you want to play another round? (Y/N): ').upper()
            if play_again != 'Y':
                break
    
    def offer_insurance(self):
        for player in self.players:
            if self.dealer_hand.cards[0].rank == 'A':
                while True:
                    insurance_bet = input(f"{player.name}, Dealer shows an Ace. Do you want to take insurance? (Y/N): ").upper()
                    if insurance_bet == 'Y':
                        insurance = player.hands[0].bet / 2
                        if self.dealer_blackjack:
                            player.update_bankroll(insurance)
                            print(f"{player.name} wins insurance! Dealer has Blackjack.")
                        else:
                            player.update_bankroll(-insurance)
                            print(f"{player.name} loses insurance. Dealer does not have Blackjack.")
                        break
                    elif insurance_bet == 'N':
                        break
                    else:
                        print("Invalid input. Please choose 'Y' or 'N'.")

    def side_bets(self):
        for player in self.players:
            while True:
                side_bet = input(f"{player.name}, do you want to place a side bet? (Y/N): ").upper()
                if side_bet == 'Y':
                    bet_amount = int(input(f"Place your side bet amount: "))
                    if 0 < bet_amount <= player.bankroll:
                        player.update_bankroll(-bet_amount)
                        print(f"{player.name} placed a side bet of ${bet_amount}.")
                        # Add side bet logic here (e.g., odds for specific card combinations)
                        # For now, let's assume a simple side bet outcome
                        if random.choice([True, False]):
                            player.update_bankroll(bet_amount * 2)  # Win side bet
                            print(f"{player.name} won the side bet!")
                        else:
                            print(f"{player.name} lost the side bet.")
                        break
                    else:
                        print(f"Invalid bet amount. You have ${player.bankroll}.")
                elif side_bet == 'N':
                    break
                else:
                    print("Invalid input. Please choose 'Y' or 'N'.")

# Example usage
if __name__ == "__main__":
    game = PokerGame()
    game.add_player('Alice', 1000)
    game.add_player('Bob', 1000)
    game.play()
