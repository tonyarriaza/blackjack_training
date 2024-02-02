import random

class BlackjackGame:
    def __init__(self, number_of_decks=1):
        self.number_of_decks = number_of_decks
        self.shoe = self.create_shoe()
        self.player_hands = [[]]
        self.dealer_hand = []
        self.current_hand = 0  # Index of the current player hand being played
        self.game_state = "PLAYING"  # Can be PLAYING, PLAYER_BUST, DEALER_BUST, PLAYER_WIN, DEALER_WIN, PUSH
        self.split_allowed = True  # Tracks if the player can split (only once per round for simplicity)

    def create_shoe(self):
        """Creates and shuffles the shoe with the specified number of decks."""
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'rank': rank, 'value': min(10, int(rank) if rank.isdigit() else 10), 'ace': rank == 'A'} for rank in ranks] * 4
        shoe = deck * self.number_of_decks
        random.shuffle(shoe)
        return shoe

    def deal_card(self, hand):
        """Deals a single card from the shoe to a given hand."""
        if len(self.shoe) < 20:  # Reshuffle if the shoe is low
            self.shoe = self.create_shoe()
            print("Shoe reshuffled.")
        card = self.shoe.pop()
        hand.append(card)

    def calculate_hand_value(self, hand):
        """Calculates the value of a hand, accounting for Aces as 11 or 1."""
        value, aces = 0, 0
        for card in hand:
            value += card['value']
            if card['ace']:
                aces += 1
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def show_hands(self, reveal_dealer=False):
        """Displays the player's and dealer's hands. Dealer's first card is hidden unless reveal_dealer is True."""
        dealer_hand = "Dealer: [" + ", ".join(card['rank'] for card in self.dealer_hand[1:]) + ", ??]" if not reveal_dealer else "Dealer: [" + ", ".join(card['rank'] for card in self.dealer_hand) + "]"
        print(dealer_hand + " Value: " + str(self.calculate_hand_value(self.dealer_hand) if reveal_dealer else "?"))
        for index, hand in enumerate(self.player_hands):
            hand_str = "Player Hand " + str(index+1) + ": [" + ", ".join(card['rank'] for card in hand) + "] Value: " + str(self.calculate_hand_value(hand))
            print(hand_str)

    def check_for_blackjack(self):
        dealer_blackjack = self.calculate_hand_value(self.dealer_hand) == 21
        player_blackjacks = [self.calculate_hand_value(hand) == 21 for hand in self.player_hands]

        if dealer_blackjack and any(player_blackjacks):
            self.game_state = "PUSH"
        elif any(player_blackjacks):
            self.game_state = "PLAYER_WIN"
        elif dealer_blackjack:
            self.game_state = "DEALER_WIN"

    def player_action(self, action, hand_index):
        hand = self.player_hands[hand_index]
        if action == "h":
            self.deal_card(hand)
            if self.calculate_hand_value(hand) > 21:
                print(f"Player Hand {hand_index + 1} busts.")
                if hand_index + 1 == len(self.player_hands):  # Last hand
                    self.game_state = "PLAYER_BUST"
        elif action == "s":
            return  # Player stands; move to next hand or dealer turn
        elif action == "d" and len(hand) == 2:  # Double down condition
            self.deal_card(hand)
            print(f"Player doubles down on Hand {hand_index + 1}.")
            if self.calculate_hand_value(hand) > 21:
                print(f"Player Hand {hand_index + 1} busts.")
            if hand_index + 1 == len(self.player_hands):  # Last hand
                self.game_state = "PLAYER_BUST"
            return  # Move to next hand or dealer turn after doubling down
        elif action == "sp" and self.split_allowed and len(hand) == 2 and hand[0]['rank'] == hand[1]['rank']:
            self.player_hands.append([self.player_hands[hand_index].pop()])
            self.deal_card(self.player_hands[hand_index])
            self.deal_card(self.player_hands[-1])
            self.split_allowed = False  # Only allow one split per game for simplicity
            print(f"Player splits Hand {hand_index + 1}.")
            return  # Allow additional actions on the new hands

    def player_turn(self):
        for index, hand in enumerate(self.player_hands):
            while self.game_state == "PLAYING":
                self.show_hands()
                action = input(f"Hand {index + 1}: Do you want to (h)it, (s)tand, (d)ouble down, or s(p)lit? ").lower()
                if action in ["h", "s", "d", "sp"]:
                    self.player_action(action, index)
                    if action in ["s", "d", "sp"]:
                        break  # Move to next hand or dealer turn
                else:
                    print("Invalid action. Please choose 'h', 's', 'd', or 'sp'.")

    def dealer_turn(self):
        if self.game_state == "PLAYING":
            while self.calculate_hand_value(self.dealer_hand) < 17:
                self.deal_card(self.dealer_hand)
            if self.calculate_hand_value(self.dealer_hand) > 21:
                self.game_state = "DEALER_BUST"

    def compare_hands(self):
        if self.game_state not in ["PLAYER_BUST", "DEALER_BUST"]:
            dealer_value = self.calculate_hand_value(self.dealer_hand)
            for index, hand in enumerate(self.player_hands):
                player_value = self.calculate_hand_value(hand)
                if player_value > dealer_value:
                    print(f"Player Hand {index + 1} wins.")
                elif player_value < dealer_value:
                    print(f"Player Hand {index + 1} loses.")
                else:
                    print(f"Player Hand {index + 1} pushes.")

    def play_game(self):
        # Initial deal
        self.deal_card(self.player_hands[0])
        self.deal_card(self.dealer_hand)
        self.deal_card(self.player_hands[0])
        self.deal_card(self.dealer_hand)

        # Check for Blackjack
        self.check_for_blackjack()

        # Player turn
        if self.game_state == "PLAYING":
            self.player_turn()

        # Dealer turn
        self.dealer_turn()

        # Compare hands
        self.compare_hands()

        # Show result
        self.show_hands(reveal_dealer=True)

        # Reset for next game
        self.player_hands = [[]]
        self.dealer_hand = []
        self.game_state = "PLAYING"
        self.split_allowed = True

# Example usage
game = BlackjackGame(number_of_decks=2)
game.play_game()
