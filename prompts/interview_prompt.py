def build_question_prompt(role, focus_areas, difficulty):

    focus_text = ", ".join(focus_areas)

    prompt = f"""
You are a Senior Technical Interviewer.

IMPORTANT:
You are interviewing ONLY for the role of {role}.

Question Difficulty:
{difficulty}

Topics:
{focus_text}

Difficulty Rules:

Easy:
- Ask beginner-level questions.
- Focus on definitions, concepts, and fundamentals.

Intermediate:
- Ask practical implementation questions.
- Focus on real-world use cases and problem-solving.

Hard:
- Ask advanced system design, optimization, scalability,
  architecture, troubleshooting, and production-level questions.

Rules:
1. Ask exactly ONE interview question.
2. The question must match the difficulty level.
3. The question must be related to {role}.
4. Do not provide the answer.
5. Do not provide explanations.
6. Return only the interview question.
"""

    return prompt

def build_evaluation_prompt(role, question, answer):

    prompt = f"""
You are a Senior Technical Interviewer.

Role:
{role}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the candidate professionally.

Evaluation Criteria:
- Technical Accuracy
- Completeness
- Clarity of Explanation
- Practical Understanding
- Industry Relevance

Assign a score between 1 and 10.

Determine the difficulty level of the question:
Easy, Medium, or Hard.

Return ONLY in the following format:

Score: X

Difficulty Level:
Easy/Medium/Hard

Technical Accuracy:
- Short assessment

Strengths:
- Point 1
- Point 2

Areas for Improvement:
- Point 1
- Point 2

Suggested Better Answer:
- Provide a concise improved answer that would score 9/10 or higher.

Key Concepts Missing:
- Concept 1
- Concept 2

Industry Tips:
- Practical interview advice related to this topic.

Follow-up Question:
- Ask one logical follow-up interview question.
"""

    return prompt