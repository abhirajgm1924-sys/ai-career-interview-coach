# Test Scenarios

Manual scenarios to walk through after running `streamlit run app.py`.
Check these whenever app.py, ui/dashboard.py, or the interview/ modules
change, until an automated test suite is added.

Prerequisite: Ollama must be running locally with `gemma3:4b` pulled
(`ollama list` should show it) — these scenarios assume that's already set up.

## 1. App starts with no errors
- **Steps:** Run `streamlit run app.py`.
- **Expected:** Page loads with the title "AI Career Interview Coach", a
  role dropdown, a difficulty dropdown, and Chat/Dashboard navigation in
  the sidebar. No import errors or crashes in the terminal.

## 2. Role list matches what's actually defined
- **Steps:** Open the role dropdown.
- **Expected:** Only roles defined in `interview/questions.py` (ROLES dict)
  appear — selecting any of them should not throw a KeyError. If a role is
  added to the dropdown but not to ROLES, this is the test that should
  catch it.

## 3. First question generates correctly
- **Steps:** Select a role and difficulty, go to the Chat tab.
- **Expected:** After a short delay (model runs locally), an AI-generated
  question relevant to the selected role and difficulty appears as the
  first assistant message. Check it isn't empty, garbled, or generic
  boilerplate unrelated to the role.

## 4. Submitting an answer produces real feedback
- **Steps:** Type an answer to the question and submit.
- **Expected:**
  - Your answer appears as a user message.
  - After a delay, a feedback message appears containing a "Score: X"
    line, strengths/areas for improvement, and a follow-up question
    (per the format in `prompts/interview_prompt.py`).
  - A new question is generated automatically right after, continuing
    the interview.

## 5. Dashboard reflects real scores
- **Steps:** After answering at least 2-3 questions, switch to the
  Dashboard tab.
- **Expected:**
  - "Questions answered" matches the number of answers you submitted.
  - "Latest score" matches the score from your most recent answer.
  - "Average score" is the correct mean of all scores so far.
  - The line chart has one point per answered question.
  - Expanding a question in "Detailed feedback" shows your answer and
    the full feedback text for that turn.

## 6. Empty dashboard state
- **Steps:** Open the Dashboard tab before answering any questions.
- **Expected:** A message saying there's no interview data yet — no
  error, no broken chart.

## 7. Score extraction handles malformed model output
- **Steps:** Hard to trigger manually, but worth knowing: if the model's
  response doesn't contain a line like "Score: 7", `extract_score()` in
  `interview/score.py` returns 0 rather than crashing.
- **Expected:** If you ever see a 0 score where you'd expect higher, check
  the raw feedback text (in the Dashboard's expander) to see if the model
  actually followed the expected format — this is a useful tool for
  debugging prompt issues, not necessarily a bug in the score logic.

## 8. Fresh machine run (the real "does it run for the lead" test)
- **Steps:** On a clean machine or environment:
  1. Install Ollama, run `ollama pull gemma3:4b`.
  2. Clone the repo, checkout `dev`.
  3. `pip install -r requirements.txt`.
  4. `streamlit run app.py`.
- **Expected:** App starts and the full flow (steps 3-5 above) works with
  no missing-dependency or import errors. This is the scenario that
  actually matters for "push it so he can run it."