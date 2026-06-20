import ollama

from interview import questions as qs
from prompts.interview_prompt import build_question_prompt
from prompts.interview_prompt import build_evaluation_prompt

def generate_question(role, difficulty):

    focus_areas = qs.ROLES[role]["focus_areas"]

    prompt = build_question_prompt(
        role,
        focus_areas,
        difficulty
    )

    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]

def evaluate_answer(role, question, answer):
    
    prompt = build_evaluation_prompt(
        role,
        question,
        answer
    )

    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    report = response["message"]["content"]

    return report


