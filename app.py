"""
AI Career Interview Coach - main Streamlit app.

Wires the Streamlit UI / chat / session state / dashboard to the existing
interview backend (interview/questions.py, interview/evaluator.py,
interview/score.py, prompts/interview_prompt.py), which uses Ollama
(model: gemma3:4b) to generate questions and evaluate answers.

Requires Ollama installed and running locally, with the gemma3:4b model
pulled (`ollama pull gemma3:4b`) — this is separate from the pip
dependencies in requirements.txt.

Run with:
    streamlit run app.py
"""

import streamlit as st

from interview import questions as qs
from interview.evaluator import generate_question, evaluate_answer
from interview.score import extract_score, calculate_average
from ui.dashboard import render_dashboard


def init_session_state():
    """Set up everything that needs to persist across Streamlit reruns."""
    if "messages" not in st.session_state:
        # Chat transcript shown in the UI: {"role": "user"|"assistant", "content": str}
        st.session_state.messages = []

    if "current_question" not in st.session_state:
        st.session_state.current_question = None

    if "feedback_history" not in st.session_state:
        # One entry per answered question, used by the dashboard:
        # {"question": str, "answer": str, "feedback": str, "score": int}
        st.session_state.feedback_history = []

    if "interview_ended" not in st.session_state:
        st.session_state.interview_ended = False


def render_chat(role, difficulty):
    st.subheader("Mock Interview Chat")

    # Generate the first question for this session if we don't have one yet
    # (and the interview hasn't been ended).
    if st.session_state.current_question is None and not st.session_state.interview_ended:
        with st.spinner("Generating your interview question..."):
            question = generate_question(role, difficulty)
        st.session_state.current_question = question
        st.session_state.messages.append({"role": "assistant", "content": question})

    # Replay the conversation so far.
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if st.session_state.interview_ended:
        st.info("Interview ended. Check the Dashboard tab for your final report.")
        return

    answer = st.chat_input("Type your answer...")
    if answer:
        # 1. Show the candidate's answer.
        st.session_state.messages.append({"role": "user", "content": answer})
        with st.chat_message("user"):
            st.markdown(answer)

        # 2. Evaluate it against the question that was asked.
        with st.spinner("Evaluating your answer..."):
            feedback = evaluate_answer(role, st.session_state.current_question, answer)
        score = extract_score(feedback)

        st.session_state.feedback_history.append(
            {
                "question": st.session_state.current_question,
                "answer": answer,
                "feedback": feedback,
                "score": score,
            }
        )

        with st.chat_message("assistant"):
            st.markdown(feedback)
        st.session_state.messages.append({"role": "assistant", "content": feedback})

        # 3. Move on to the next question.
        with st.spinner("Preparing next question..."):
            next_question = generate_question(role, difficulty)
        st.session_state.current_question = next_question
        st.session_state.messages.append({"role": "assistant", "content": next_question})


def main():
    st.set_page_config(page_title="AI Career Interview Coach", layout="wide")
    init_session_state()

    st.title("AI Career Interview Coach")

    # Pull roles dynamically from questions.py so the dropdown can never
    # offer a role that ROLES doesn't actually define (that would crash
    # generate_question with a KeyError).
    available_roles = list(qs.ROLES.keys())
    role = st.sidebar.selectbox("Select Role", available_roles)
    difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Intermediate", "Hard"])

    # Changing role/difficulty mid-session currently doesn't reset the
    # in-progress question — fine for now, worth revisiting later.
    page = st.sidebar.radio("Navigate", ["Chat", "Dashboard"])

    st.sidebar.divider()
    if not st.session_state.interview_ended:
        if st.sidebar.button("End Interview"):
            st.session_state.interview_ended = True
            st.rerun()
    else:
        if st.sidebar.button("Start New Interview"):
            st.session_state.messages = []
            st.session_state.current_question = None
            st.session_state.feedback_history = []
            st.session_state.interview_ended = False
            st.rerun()

    if page == "Chat":
        render_chat(role, difficulty)
    else:
        render_dashboard(st.session_state)


if __name__ == "__main__":
    main()