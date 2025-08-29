import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import blackjack


def test_deck_has_52_unique_cards():
    deck = blackjack.Deck()
    assert len(deck.cards) == 52
    assert len(set(deck.cards)) == 52


def test_calculate_hand_value_with_aces():
    hand = [("A", "Spades"), ("9", "Hearts")]
    assert blackjack.calculate_hand_value(hand) == 20
    hand = [("A", "Spades"), ("9", "Hearts"), ("A", "Diamonds")]
    assert blackjack.calculate_hand_value(hand) == 21


def test_deal_initial():
    game = blackjack.BlackjackGame()
    game.deal_initial()
    assert len(game.player_hand) == 2
    assert len(game.dealer_hand) == 2
    assert len(game.deck.cards) == 52 - 4
