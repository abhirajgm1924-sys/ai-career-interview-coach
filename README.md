# AI Career Interview Coach

AI-powered interview simulator for:
- Data Analyst
- Data Engineer
- Data Scientist
- Business Analyst
- Analytics Engineer
- ML Engineer

The app asks AI-generated interview questions for the selected role and
difficulty, evaluates your typed answers, and gives a score plus detailed
feedback — all tracked in a results dashboard across the session.

## Architecture

```
User -> Streamlit UI -> Interview Engine -> Ollama -> Evaluation Engine -> Feedback + Score
```

- **Streamlit UI** (`app.py`, `ui/dashboard.py`) — chat interface, session
  state, results dashboard.
- **Interview Engine** (`interview/questions.py`, `interview/evaluator.py`,
  `prompts/interview_prompt.py`) — builds prompts and calls the model to
  generate questions and evaluate answers.
- **Ollama** — runs the model (`gemma3:4b`) locally.
- **Score extraction** (`interview/score.py`) — parses the model's
  feedback text into a numeric score and computes session averages.

## Project structure

```
.
├── app.py                       # Main entrypoint: role/difficulty select, chat, nav
├── ui/
│   └── dashboard.py              # Results dashboard, reads session feedback_history
├── interview/
│   ├── questions.py               # ROLES: focus areas per role
│   ├── evaluator.py               # generate_question(), evaluate_answer() — calls Ollama
│   └── score.py                   # extract_score(), calculate_average()
├── prompts/
│   └── interview_prompt.py        # Prompt templates for question generation + evaluation
├── tests/
│   └── test_scenarios.md
├── requirements.txt
└── README.md
```

## Setup

### 1. Install Ollama (required — separate from pip)

Download and install from [ollama.com/download](https://ollama.com/download).
This runs the model locally; it is **not** installed via pip.

After installing, open a fresh terminal (so it picks up the new PATH) and
pull the model used by this project:

```bash
ollama pull gemma3:4b
```

Confirm it's available:

```bash
ollama list
```

You should see `gemma3:4b` listed. The app will fail at runtime if Ollama
isn't installed and running, or if this model hasn't been pulled.

### 2. Clone the repo and switch to the `dev` branch

```bash
git clone <repo-url>
cd ai-career-interview-coach
git checkout dev
git pull origin dev
```

### 3. (Recommended) Create a virtual environment

```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash / Mac / Linux
venv\Scripts\activate          # Windows Command Prompt
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

## Running the app

```bash
streamlit run app.py
```

Opens in your browser, usually at `http://localhost:8501`. Select a role
and difficulty, then use the Chat tab — the first question generates
automatically (may take a few seconds since the model runs locally).
Answer it to get real feedback and a score, then check the Dashboard tab
to see your session results.

## Known limitations / next steps

- Changing role or difficulty mid-session doesn't reset the
  in-progress question.
- No final assessment report yet (per-question feedback and a running
  average exist; a generated end-of-session summary does not).
- No automated test suite yet — see `tests/test_scenarios.md` for the
  manual scenarios to check after changes.
