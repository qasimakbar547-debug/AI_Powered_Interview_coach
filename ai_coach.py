def evaluate_answer(question, answer):
    """Demo evaluation without API."""

    answer = answer.strip()

    if not answer:
        return {
            "score": 0,
            "grammar_correction": "No answer was provided.",
            "feedback": "Please provide an answer.",
            "better_answer": "Please write a complete answer."
        }

    word_count = len(answer.split())

    if word_count < 10:
        score = 4
        feedback = (
            "Your answer is quite short. "
            "Try to add more details and an example."
        )

    elif word_count < 25:
        score = 6
        feedback = (
            "Good start. Add more details and make your answer "
            "more professional."
        )

    elif word_count < 50:
        score = 8
        feedback = (
            "Good answer. You explained your point clearly. "
            "Try to add a practical example."
        )

    else:
        score = 9
        feedback = (
            "Very good answer. Your answer has good detail. "
            "Keep it focused and professional."
        )

    return {
        "score": score,
        "grammar_correction": (
            "Demo Mode: Real AI grammar correction is not connected yet."
        ),
        "feedback": feedback,
        "better_answer": (
            "A stronger answer should clearly explain your point, "
            "give a short example, and connect your experience "
            "with the job."
        )
    }


def generate_final_report(results):
    """Generate final demo report without API."""

    if not results:
        return "No interview results are available."

    scores = []

    for result in results:
        try:
            scores.append(float(result.get("score", 0)))
        except (ValueError, TypeError):
            scores.append(0)

    average_score = sum(scores) / len(scores)

    if average_score >= 8:
        performance = "Very Good"
    elif average_score >= 6:
        performance = "Good"
    elif average_score >= 4:
        performance = "Needs Improvement"
    else:
        performance = "Needs Significant Improvement"

    report = f"""
# 🎤 Final Interview Report

## Overall Performance
{performance}

## Average Score
{average_score:.1f} / 10

## Strong Areas
- You attempted the interview questions.
- You provided answers for evaluation.
- You can improve your answers with more examples.

## Weak Areas
- Some answers need more detail.
- Organize your answers clearly.
- Practice professional English.

## English Improvement
- Use short and clear sentences.
- Practice grammar and sentence structure.
- Practice speaking regularly.

## Technical Improvement
- Review concepts related to your interview category.
- Explain technical concepts in simple words.
- Add practical examples.

## Practical Next Steps
1. Practice 5 interview questions every day.
2. Give examples from your projects or studies.
3. Improve your English answers gradually.
4. Practice again and try to increase your score.

---

⚠️ DEMO MODE

Real AI evaluation can be connected later using an API.
"""

    return report