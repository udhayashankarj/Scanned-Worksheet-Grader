def build_evaluation_prompt(answer_key, ocr_results) -> str:
    qa_pairs = []
    for q in answer_key.questions:
        student_ans = next(
            (a["student_answer"] for a in ocr_results["answers"] if a["question_number"] == q.question_number),
            "No answer provided"
        )
        qa_pairs.append(
            f"Q{q.question_number} [{q.max_marks} marks]: {q.question}\n"
            f"  Expected: {q.expected_answer}\n"
            f"  Student wrote: {student_ans}"
        )

    pairs_text = "\n\n".join(qa_pairs)

    return f"""You are an expert examiner for {answer_key.subject}.

Evaluate each student answer against the expected answer and assign marks.

{pairs_text}

Scoring Guidelines:
- Full marks: Answer is complete, accurate, and covers all key points
- Partial marks: Answer is partially correct or missing some key points  
- Zero marks: Answer is wrong, blank, or completely irrelevant

Return ONLY a valid JSON object (no markdown, no backticks, no explanation):
{{
  "overall_feedback": "2-3 sentence overall assessment of the student's performance",
  "evaluations": [
    {{
      "question_number": 1,
      "student_answer": "what student wrote",
      "marks_awarded": 4,
      "feedback": "specific 1-2 sentence feedback explaining the score"
    }}
  ]
}}"""