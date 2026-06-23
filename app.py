import streamlit as st

# FIX: Separated game logic from UI — pulled the rules into logic_utils.py
# with Claude in agent mode while I directed the refactor.
import logic_utils as game

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Now de-glitched.")

# --- Settings (sidebar) ---
st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = game.get_attempt_limit(difficulty)
low, high = game.get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


# FIX: New Game now fully resets. Claude and I traced that the old reset used
# attempts=0 while init used attempts=1 (inconsistent start) and never cleared
# the guess box — one shared function + an input nonce fixes both.
def start_new_game():
    """Reset every piece of game state to a clean starting point."""
    st.session_state.secret = game.new_secret(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.feedback = None
    st.session_state.celebrate = False
    # Bump the input nonce so the guess text box is rendered fresh (empty).
    st.session_state.input_nonce = st.session_state.get("input_nonce", 0) + 1


# Initialise state on first load.
if "secret" not in st.session_state:
    start_new_game()


# FIX: Claude spotted the root cause of the counter bugs — state was mutated
# AFTER the UI rendered, so the banner was always one step stale. We moved all
# state changes into this function, which runs before the rerun/redraw. This
# kills bugs 3, 4 and 5 (inconsistent counter, no decrease on first guess, and
# "1 left" + "out of attempts" showing together).
def process_guess(raw_guess, show_hint):
    """Validate and apply a guess, mutating session state.

    All state changes happen here BEFORE the UI is (re)rendered, so the
    displayed attempts/status are never one step stale.
    """
    if st.session_state.status != "playing":
        st.session_state.feedback = ("warning", "Game over — start a New Game.")
        return

    ok, guess_int, err = game.parse_guess(raw_guess)
    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.feedback = ("error", err)
        return

    # FIX: count the guess first, then evaluate it — this is what makes the
    # attempts counter tick down on the very first guess (bug 4).
    st.session_state.attempts += 1
    st.session_state.history.append(guess_int)

    # FIX: the wrong-hint bug. Claude found the old code stringified the secret
    # on even turns, causing a lexicographic / inverted comparison. check_guess
    # now compares numerically, and the hint text is derived from the outcome.
    outcome = game.check_guess(guess_int, st.session_state.secret)
    message = game.hint_for_outcome(outcome)
    st.session_state.score = game.update_score(
        current_score=st.session_state.score,
        outcome=outcome,
        attempt_number=st.session_state.attempts,
    )

    if outcome == "Win":
        st.session_state.status = "won"
        st.session_state.celebrate = True
        st.session_state.feedback = (
            "success",
            f"🎉 You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}",
        )
    elif st.session_state.attempts >= attempt_limit:
        st.session_state.status = "lost"
        st.session_state.feedback = (
            "error",
            f"Out of attempts! The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}",
        )
    elif show_hint:
        st.session_state.feedback = ("warning", message)
    else:
        st.session_state.feedback = ("info", "Not quite — keep going.")


# --- Status banner (rendered from the FINAL, post-guess state) ---
# FIX (bug 5): Claude and I made this branch on the final status, so "Attempts
# left" only shows while playing — it can no longer appear next to "Game over".
st.subheader("Make a guess")

attempts_left = max(attempt_limit - st.session_state.attempts, 0)
playing = st.session_state.status == "playing"

if playing:
    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempts_left}"
    )
elif st.session_state.status == "won":
    st.success("You already won. Start a New Game to play again.")
else:
    st.error("Game over. Start a New Game to try again.")

# One-shot celebration after a winning rerun.
if st.session_state.get("celebrate"):
    st.balloons()
    st.session_state.celebrate = False

# Transient feedback from the last action (hint / result / error).
feedback = st.session_state.get("feedback")
if feedback:
    kind, text = feedback
    getattr(st, kind)(text)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Status:", st.session_state.status)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# --- Input + controls ---
raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{st.session_state.input_nonce}",
    disabled=not playing,
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀", disabled=not playing)
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: the pattern Claude recommended and I approved — handle input, mutate
# state, then st.rerun() so every widget above redraws from the final state.
# --- Handlers: mutate state, then rerun so the UI reflects final state ---
if new_game:
    start_new_game()
    st.rerun()

if submit:
    process_guess(raw_guess, show_hint)
    st.rerun()

st.divider()
st.caption("Built by an AI — and since debugged by a human.")
