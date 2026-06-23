# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
When I first ran the game, I noticed several issues that affected gameplay. The New Game button did not start a new game when clicked. The guessing hints were also incorrect; when I entered a number lower than the target number, the game sometimes told me to guess lower instead of higher. In addition, the attempts counter was inconsistent because the top of the page showed attempts remaining while the bottom of the page reported that I was out of attempts and revealed the answer. I also noticed that the first guess did not reduce the attempts count, and the score calculation appeared inconsistent throughout the game

- What did the game look like the first time you ran it? Normal. Like it had no glitches.
- List at least two concrete bugs you noticed at the start  
New game feature did not work
The hints feature was very innacurate
  (for example: "the hints were backwards").

**Bug Reproduction Log**
| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|------------------|----------------|----------------------|
| Clicked "New Game" button | A new game should start and reset all values | Nothing happened; the game did not restart | None |
| Guessed a number lower than the correct answer | Game should display "Go Higher" | Game displayed "Go Lower" | None |
| Used all available attempts | Attempts counter should reach 0 consistently and end the game | Top counter showed 1 attempt left while bottom message said "Out of Attempts" and revealed the answer | None |
| Made first guess of the game | Attempts should decrease immediately | First guess did not reduce the attempts count | None |
| Played multiple rounds and compared scores | Score should be calculated consistently based on performance | Score changed inconsistently and did not match expected results | None |
Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| | | | |
| | | | |
| | | | |

---

## 2. How did you use AI as a teammate?

**Which AI tool I used:** I used Claude (Claude Code) running in agent mode inside my code editor. It could read my files, make edits, and run my tests for me while I told it what I wanted and checked its work.

**One thing the AI got correct:** Claude figured out that all my attempts-counter bugs came from the same root problem. The game was changing things like the attempts count *after* it had already drawn the screen, so the screen always showed the old number, one step behind. Claude moved all the number-changing code so it runs *before* the screen gets drawn, and then told the app to refresh. I checked this by playing the game: the counter went down right on my first guess, and I never again saw "1 attempt left" and "out of attempts" showing at the same time. So that fix was real.

**One thing the AI said that was misleading:** When Claude first explained the backwards-hint bug, it told me the old code "compared the numbers as text," like "9" looking bigger than "100." That sounded clean and made sense, but it was a little misleading. In Python, comparing a number to text does not quietly give a wrong answer, it actually crashes the line. The text comparison only happened in a hidden backup part of the code that ran *after* the crash, and that backup part also had the hint messages typed in backwards. So the real story was messier than the simple version Claude gave me at first. I caught this by going back through the original code with the AI and asking it to walk through what actually happens line by line.

**Another slightly misleading thing:** Right after Claude started the game, it said the app was "running and serving correctly." But all it had really checked was that the web server answered (an HTTP 200 response). That only means the page loaded, not that the hints, counter, or New Game button actually worked. The app behaving correctly was something *I* proved by playing it, not something the server check proved.

---

## 3. Debugging and testing your fixes

**How I decided a bug was really fixed:** Mostly by playing the game myself after each change. For the hint bug I typed a number lower than the answer and made sure it told me to go higher, then a number higher than the answer and made sure it told me to go lower. I did this several times in a row on purpose, because the old bug only showed up on every other guess. When the hints stayed correct every time, I knew it was fixed.

**One test I ran:** I opened my terminal and ran pytest (`python -m pytest`). It showed "9 passed." Three of those were the starter tests that already came with the project, and six were new tests the AI wrote with me that aim straight at the backwards-hint bug. One of the new tests even recreates the exact weird case that used to break it, where the answer was stored as text instead of a number.

**An honest catch about the tests:** Those tests only check the plain game rules (the math functions). They do NOT test the buttons, the counter, or the New Game reset, because that stuff is Streamlit screen behavior. So "9 passed" did not actually prove those bugs were fixed. The only thing that proved the New Game button, the counter, and the no-double-message fixes worked was me playing the game in the browser and watching everything behave the right way.

**Did AI help with tests:** Yes. Claude wrote the six new tests and explained why each one mattered, especially the one that copies the original bug on purpose so it can never sneak back in later.

---

## 4. What did you learn about Streamlit and state?

The biggest thing I learned is that Streamlit re-runs my whole code file from top to bottom every single time I click something. It's like the page rebuilds itself from scratch on every click. Because of that, normal variables forget their values between clicks. The lesson that really stuck was about order: if you draw the screen first and change the numbers after, the screen shows old info. You have to update the numbers first, then draw the screen.

---

## 5. Looking ahead: your developer habits

**One habit I want to keep:** Testing by actually using the thing, not just trusting that it looks done. I also liked having small tests that re-check the exact bug, so it can't quietly come back later.

**One thing I'd do differently with AI:** I'd slow the AI down sooner and ask it to walk me through what actually happens step by step. Its first explanation of the hint bug sounded confident and clean but was a little off, and asking "walk me through what really happens" got me the true answer.

**How this changed how I think about AI code:** It showed me that AI code and AI explanations can sound very confident and still be partly wrong or oversimplified. It's a great teammate for finding and fixing things fast, but I still have to test it myself and ask follow-up questions instead of just trusting whatever it says.
