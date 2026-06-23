"""Pure game logic for the number guessing game.

No Streamlit / UI code lives here so the rules can be reasoned about and
unit-tested in isolation. The UI layer (app.py) owns all session state and
rendering; it calls into these functions.
"""

import random


# Inclusive (low, high) range per difficulty.
DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 50),
}

# How many guesses the player gets per difficulty.
ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive (low, high) range for a given difficulty."""
    return DIFFICULTY_RANGES.get(difficulty, (1, 100))


def get_attempt_limit(difficulty: str):
    """Return the number of allowed guesses for a given difficulty."""
    return ATTEMPT_LIMITS.get(difficulty, 8)


def new_secret(low: int, high: int, rng=random):
    """Pick a fresh secret number in the inclusive [low, high] range."""
    return rng.randint(low, high)


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    On success guess_int is an int and error_message is None; on failure
    guess_int is None and error_message explains why.
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    text = raw.strip()
    try:
        # Accept "42" and "42.0" but reject genuinely non-numeric input.
        value = int(float(text)) if "." in text else int(text)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    outcome is one of: "Win", "Too High", "Too Low".
    Both values are coerced to int and compared numerically so the result
    is always correct (a string secret no longer triggers a lexicographic
    comparison or an inverted hint).
    """
    # FIX: the inverted-hint bug. I flagged the wrong hints; Claude found the
    # secret was being stringified upstream, breaking the comparison. Coercing
    # both to int here makes the comparison numeric and the hint reliable.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


# FIX: Claude suggested deriving the hint text from the outcome via this map,
# which I agreed to — the direction can never drift out of sync with the
# outcome again (the old code hard-coded inverted messages in places).
# Directional hint shown to the player for each outcome.
HINTS = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def hint_for_outcome(outcome: str):
    """Return the directional hint message for an outcome."""
    return HINTS.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    A win earns more the earlier it happens (minimum 10). Any wrong guess
    costs a flat, consistent penalty.
    """
    # FIX: scoring made consistent. Claude noticed the old code secretly ADDED
    # points for a "Too High" guess on even attempts; we agreed every wrong
    # guess should cost the same flat penalty.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    # Too High / Too Low: a wrong guess always costs the same.
    return current_score - 5
