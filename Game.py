from random import shuffle

NUM_DECKS = 1

class Deck:

    card_ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    card_suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']

    def __init__(self):
        self.cards = []
        self.cards_backup = []
        self.new_deck()
        self.make_backup()

    def new_deck(self):
        for deck_num in range(0, NUM_DECKS):
            for card_suit in self.card_suits:
                for card_rank in self.card_ranks:
                    self.cards.append((card_rank, card_suit, deck_num))

    def make_backup(self):
        for deck_num in range(0, NUM_DECKS):
            for card_suit in self.card_suits:
                for card_rank in self.card_ranks:
                    self.cards_backup.append((card_rank, card_suit, deck_num))

    def get_backup(self):
        return self.cards_backup

    def get_deck(self):
        return self.cards

    def shuffle(self):
        shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def lis_deck(self):
        return self.cards

    def cards_remaining(self):
        return len(self.cards)

    def deck_length(self):
        return NUM_DECKS*52

    def num_decks(self):
        return self.deck_length()/52


class Player:

    def __init__(self):
        self.hand = []
        self.hand_value = 0
        self.standing = 0

    def add_card(self, card):
        self.hand.append(card)
        self.calculate_hand_value()

    def get_hand(self):
        return self.hand

    def calculate_hand_value(self):
        self.hand_value = 0
        ace_count = 0
        for card in self.hand:
            if card[0] == 'Ace':
                ace_count += 1
            elif card[0] in {'J', 'Q', 'K'}:
                self.hand_value += 10
            else:
                self.hand_value += int(card[0])
        if ace_count:
            if (self.hand_value + 11) <= (21 - (ace_count - 1)):
                self.hand_value += 11
                for x in range(0, ace_count-1):
                    self.hand_value += 1
            else:
                for x in range(0, ace_count):
                    self.hand_value += 1


    def get_hand_value(self):
        return self.hand_value

    def stood(self):
        self.standing = 1


class Dealer:

    def __init__(self):
        self.hand = []
        self.turn = 0
        self.standing = 0

    def add_card(self, card):
        self.hand.append(card)

    def get_hand(self):
        if self.turn < 3:
            return self.hand[1:]
        else:
            return self.hand

    def calculate_hand_value(self):
        hand_value = 0
        for card in self.get_hand():
            if card[0] == 'Ace':
                if hand_value < 16:
                    hand_value += 1
                else:
                    hand_value += 11
            elif card[0] in {'J', 'Q', 'K'}:
                hand_value += 10
            else:
                hand_value += int(card[0])
        return hand_value

    def get_hand_value(self):
        return self.calculate_hand_value()

    def stood(self):
        self.standing = 1


class BlackJack:

    def __init__(self):
        self.game_deck = Deck()
        self.game_deck.shuffle()
        self.next_game()

    def next_game(self):
        self.dealer = Dealer()
        self.player = Player()
        self.turn = 0
        if self.game_deck.cards_remaining() < (NUM_DECKS*52*(1/2)):
            self.game_deck = Deck()
            self.game_deck.shuffle()
        self.start()

    def start(self):
        for x in range(0, 2):
            self.dealer.add_card(self.game_deck.draw_card())
            self.dealer.turn += 1
            self.player.add_card(self.game_deck.draw_card())
        self.turn += 1

    def play(self, action = None):

        if action == 1:
            self.player.add_card(self.game_deck.draw_card())
        elif action == 0:
            self.player.stood()

        self.dealer_play()

        self.turn += 1

        return self.check_hands()

    def dealer_play(self):
        self.dealer.turn += 1
        if self.player.standing == 1:
            while self.dealer.get_hand_value() < 17:
                self.dealer.add_card(self.game_deck.draw_card())
            self.dealer.stood()
        elif self.dealer.get_hand_value() < 17:
            self.dealer.add_card(self.game_deck.draw_card())
        else:
            self.dealer.stood()

    def check_hands(self):
        reward = 0
        tie = False
        game_over = False

        if self.player.get_hand_value() > 21:
            reward = -100
            game_over = True
            return reward, game_over, tie

        if self.dealer.get_hand_value() > 21 or self.player.get_hand_value() == 21:
            reward = 100
            game_over = True
            return reward, game_over, tie

        if self.player.get_hand_value() > self.dealer.get_hand_value() and self.dealer.standing == 1:
            reward = 100
            game_over = True
            return reward, game_over, tie

        if self.dealer.get_hand_value() > self.player.get_hand_value() and self.player.standing == 1 and self.dealer.standing == 1:
            reward = -100
            game_over = True
            return reward, game_over, tie

        if self.dealer.get_hand_value() == self.player.get_hand_value() and self.dealer.standing == 1 and self.player.standing == 1:
            reward = 100
            game_over = True
            tie = True
            return reward, game_over, tie

        return reward, game_over, tie

    def get_game_state(self):
        state = []
        if self.dealer.get_hand_value() <= 21:
            state.append((self.dealer.get_hand_value()/21))
        else:
            state.append(0)
        if self.dealer.get_hand_value() <= 21:
            state.append((self.player.get_hand_value()/21))
        else:
            state.append(0)
        return state

    def print_hands(self):
        print('Dealer:', self.dealer.get_hand_value(), self.dealer.get_hand())
        print('Player:', self.player.get_hand_value(), self.player.get_hand())

    def get_turn(self):
        return self.turn


def main():
    game = BlackJack()
    while True:
        game.print_hands()
        selection = input("Hit or Stand: ")
        reward, game_over, tie = game.play(selection)
        if game_over:
            game.print_hands()
            if reward == 100 and tie:
                print('YOU TIED!')
            elif reward == 100 and not tie:
                print('Y0U WON!')
            else:
                print('YOU LOST!')
            print(game.dealer.get_hand_value(),'/',game.player.get_hand_value())
            game.next_game()

if __name__ == '__main__':
    main()