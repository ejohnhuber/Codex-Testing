import random
from dataclasses import dataclass, field

CARD_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


@dataclass
class Deck:
    """Represent a shuffled deck of 52 playing cards."""

    cards: list[tuple[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self) -> tuple[str, str]:
        """Remove and return the top card from the deck."""
        return self.cards.pop()


def calculate_hand_value(hand: list[tuple[str, str]]) -> int:
    """Return the best score for the given hand in blackjack."""
    value = sum(CARD_VALUES[rank] for rank, _ in hand)
    aces = sum(1 for rank, _ in hand if rank == "A")
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


class BlackjackGame:
    """Play a simple game of blackjack against an automated dealer."""

    def __init__(self) -> None:
        self.deck = Deck()
        self.player_hand: list[tuple[str, str]] = []
        self.dealer_hand: list[tuple[str, str]] = []

    def deal_initial(self) -> None:
        for _ in range(2):
            self.player_hand.append(self.deck.draw())
            self.dealer_hand.append(self.deck.draw())

    def hit(self, hand: list[tuple[str, str]]) -> None:
        hand.append(self.deck.draw())

    @staticmethod
    def format_hand(hand: list[tuple[str, str]]) -> str:
        return ", ".join(f"{rank} of {suit}" for rank, suit in hand)

    def play(self) -> None:
        self.deal_initial()
        while True:
            print(f"Dealer shows: {self.dealer_hand[0][0]} of {self.dealer_hand[0][1]}")
            player_value = calculate_hand_value(self.player_hand)
            print(
                f"Your hand: {self.format_hand(self.player_hand)} (value {player_value})"
            )
            if player_value == 21:
                print("Blackjack! You win!")
                return
            choice = input("Hit or stand? [h/s]: ").strip().lower()
            if choice.startswith("h"):
                self.hit(self.player_hand)
                player_value = calculate_hand_value(self.player_hand)
                if player_value > 21:
                    print(
                        f"You bust with {self.format_hand(self.player_hand)} (value {player_value})."
                    )
                    return
            else:
                break

        print(
            f"Dealer's hand: {self.format_hand(self.dealer_hand)} (value {calculate_hand_value(self.dealer_hand)})"
        )
        while calculate_hand_value(self.dealer_hand) < 17:
            self.hit(self.dealer_hand)
            print(
                f"Dealer hits: {self.format_hand(self.dealer_hand)} (value {calculate_hand_value(self.dealer_hand)})"
            )
            if calculate_hand_value(self.dealer_hand) > 21:
                print("Dealer busts! You win.")
                return

        player_value = calculate_hand_value(self.player_hand)
        dealer_value = calculate_hand_value(self.dealer_hand)
        print(f"Final hands - You: {player_value}, Dealer: {dealer_value}")
        if dealer_value > player_value:
            print("Dealer wins.")
        elif dealer_value < player_value:
            print("You win!")
        else:
            print("Push (tie).")


if __name__ == "__main__":
    BlackjackGame().play()
