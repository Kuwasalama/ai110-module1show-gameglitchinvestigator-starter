# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
The purpose of the game is to challenge the player to guess a randomly generated number between 1 and 100. The player is given eight attempts to find the correct number before running out of guesses. Throughout the game, hints are provided to help the player determine whether their guess is too high or too low. If the player guesses the correct number within the allowed attempts, they win the game.
- [ ] Detail which bugs you found. 
ou started working on the game?

When I first ran the game, I noticed several issues that affected gameplay. The New Game button did not start a new game when clicked. The guessing hints were sometimes incorrect, causing the game to tell the player to guess lower when the correct number was actually higher. The attempts counter was also inconsistent because the top of the page displayed attempts remaining while the bottom reported that the player was out of attempts and revealed the answer. Additionally, the first guess did not reduce the attempts count, and the score calculation appeared inconsistent throughout the game.
- [ ] Explain what fixes you applied. 
I fixed the hints so they finally point the right way, because the old code was turning the secret number into text on every other guess, which broke the comparison and flipped "go higher" and "go lower." I fixed the New Game button so it actually resets everything (the counter, score, and the typing box) instead of doing nothing. I also fixed the attempts counter by making the game update its numbers before drawing the screen, so it counts down on the very first guess and never shows "1 attempt left" and "out of attempts" at the same time. Last, I moved all the game rules into logic_utils.py so the main file just handles the screen, and I added tests to make sure the hint bug can't come back.



## 📸 Demo Walkthrough
1. Start the game.
2. Enter a guess of lets say "40".
3. The game returns "Too Low."
4. Enter a guess of "70".

5. The game returns "Too High."
6. Continue entering guesses using the hints provided by the game.
7. The score updates after each guess.
8. Enter the correct number.
9. The game displays a winning message and ends the game.
10. Click **New Game** to start a new round.

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- python.exe
cachedir: .pytest_cache
rootdir: ...\ai110-module1show-gameglitchinvestigator-starter-main
plugins: anyio-4.14.0
collecting ... collected 9 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 11%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 22%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 33%]
tests/test_hint_regression.py::test_too_high_hint_says_go_lower PASSED   [ 44%]
tests/test_hint_regression.py::test_too_low_hint_says_go_higher PASSED   [ 55%]
tests/test_hint_regression.py::test_hint_direction_is_never_inverted PASSED [ 66%]
tests/test_hint_regression.py::test_string_secret_compares_numerically_not_lexicographically PASSED [ 77%]
tests/test_hint_regression.py::test_string_secret_matches_int_secret PASSED [ 88%]
tests/test_hint_regression.py::test_winning_guess_with_string_secret PASSED [100%]

============================== 9 passed in 0.44s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
