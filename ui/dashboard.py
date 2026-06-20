"""
Results Dashboard - shows interview session metrics, built from real
feedback/score data produced by interview/evaluator.py + interview/score.py.
"""

import streamlit as st

from interview.score import calculate_average


def _performance_label(avg):
    """Translate an average score (out of 10) into a plain-language label."""
    if avg >= 8:
        return "Strong performance"
    if avg >= 6:
        return "Solid, with room to grow"
    if avg >= 4:
        return "Needs improvement"
    return "Significant gaps to address"


def render_dashboard(session_state):
    """Render the results dashboard using session_state.feedback_history.

    Each entry in feedback_history is expected to look like:
        {"question": str, "answer": str, "feedback": str, "score": int}
    """
    st.subheader("Results Dashboard")

    history = session_state.get("feedback_history", [])

    if not history:
        st.info("No interview data yet. Answer a question in the Chat tab first.")
        return

    scores = [item["score"] for item in history]
    avg = calculate_average(scores)

    if session_state.get("interview_ended"):
        st.markdown("### Final Assessment Report")
        st.write(
            f"You answered **{len(history)}** question(s) with an average "
            f"score of **{avg}/10** — {_performance_label(avg)}."
        )
        st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Questions answered", len(history))
    col2.metric("Latest score", f"{scores[-1]}/10")
    col3.metric("Average score", f"{avg}/10")

    st.divider()
    st.caption("Score trend across the session")
    st.line_chart({"Score": scores})

    st.divider()
    st.subheader("Detailed feedback")
    # Most recent first.
    for i, item in enumerate(reversed(history)):
        q_num = len(history) - i
        with st.expander(f"Q{q_num}: {item['question'][:80]}"):
            st.markdown(f"**Your answer:** {item['answer']}")
            st.markdown(item["feedback"])