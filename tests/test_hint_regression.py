"""Regression tests for the inverted-hint bug.

The original bug: on even-numbered attempts the secret was converted to a
string, so `check_guess` compared an int against a str. In Python 3 that
either raised TypeError (falling into a branch with the hint messages
inverted) or, where it didn't raise, compared the numbers lexicographically.
Either way the player could be told to "Go LOWER" when the answer was higher.

These tests lock in the fix: comparison is numeric, and the directional
hint always agrees with the outcome.
"""

from logic_utils import check_guess, hint_for_outcome


def test_too_high_hint_says_go_lower():
    # Guess above the secret -> player must go LOWER.
    assert check_guess(60, 50) == "Too High"
    assert "LOWER" in hint_for_outcome("Too High")


def test_too_low_hint_says_go_higher():
    # Guess below the secret -> player must go HIGHER.
    assert check_guess(40, 50) == "Too Low"
    assert "HIGHER" in hint_for_outcome("Too Low")


def test_hint_direction_is_never_inverted():
    # The bug surfaced as the hint pointing the wrong way. Assert the
    # outcome and its hint can never contradict each other.
    assert hint_for_outcome(check_guess(90, 10)) == "📉 Go LOWER!"   # too high
    assert hint_for_outcome(check_guess(10, 90)) == "📈 Go HIGHER!"  # too low


def test_string_secret_compares_numerically_not_lexicographically():
    # This is the exact trigger of the old bug: a string secret on even
    # attempts. 9 < 80 numerically, but "9" > "80" lexicographically.
    # The old code answered "Too High" here; the fix must say "Too Low".
    assert check_guess(9, "80") == "Too Low"
    assert check_guess(80, "9") == "Too High"


def test_string_secret_matches_int_secret():
    # A string secret must behave identically to the equivalent int secret.
    for guess in (1, 49, 50, 51, 99):
        assert check_guess(guess, "50") == check_guess(guess, 50)


def test_winning_guess_with_string_secret():
    assert check_guess(50, "50") == "Win"
    assert hint_for_outcome("Win") == "🎉 Correct!"
