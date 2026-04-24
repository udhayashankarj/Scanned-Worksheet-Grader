
def build_ocr_prompt_for_answer_key() -> str:
    return f"""You are an expert OCR system for handwritten or digital document answer keys.

The answer key contains question number, questions, answers and max marks

Extract the questions, answers and max mark for each question number.
Return ONLY a valid JSON object like this (no markdown, no backticks):
{{
  "subject": "subject name",
  "total_marks": total marks specified,
  "questions": [
    {{"question_number": 1, "question": "extracted question here", "expected_answer": "extracted answer here", "max_marks": extracted max mark here}},
    {{"question_number": 2, "question": "extracted question here", "expected_answer": "extracted answer here", "max_marks": extracted max mark here}}
  ]
}}
"""

def build_ocr_prompt_for_answer_sheet(answer_key) -> str:
    questions_list = "\n".join(
        [f"Q{q.question_number}: {q.question}" for q in answer_key.questions]
    )
    return f"""You are an expert OCR system for handwritten answer sheets.

The answer sheet contains answers to the following questions:
{questions_list}

Extract the student's handwritten answers for each question number.
Return ONLY a valid JSON object like this (no markdown, no backticks):
{{
  "answers": [
    {{"question_number": 1, "student_answer": "extracted text here"}},
    {{"question_number": 2, "student_answer": "extracted text here"}}
  ]
}}

If a question is not answered or illegible, use "No answer provided"."""

