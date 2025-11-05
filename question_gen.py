import google.generativeai as genai
import random

# --- Gemini Question Generator (v2.5-stable) ---

def generate_questions(skills):
    """
    Generates AI-based interview questions using the latest Gemini 2.5 model.
    Returns a list of question dictionaries (with type, text, and difficulty).
    """

    # Convert skill list into a readable format
    skill_text = ", ".join(skills)

    # ✅ Place your prompt INSIDE the function and properly indented
    prompt = f"""
    You are an AI interview question generator.
    Generate exactly **10 interview questions** based on: {skill_text}

    Divide them as:
    - 3 Multiple Choice Questions (MCQs)
    - 5 Pseudocode-based logical questions
    - 2 Coding questions

    For each MCQ:
    - Always include options A), B), C), D) on new lines.
    - Each option should be short and clear.
    - Include "Correct Answer:" at the end.

    For all questions:
    - Start every question with "Q:".
    - Add "Type:" and "Difficulty:" on new lines (one of Easy, Medium, Difficult).
    - Keep formatting consistent like this:

    Example:
    Q: What is a Python decorator?
    Type: MCQ
    Difficulty: Medium
    A) A special syntax for loops
    B) A function that modifies another function
    C) A Python library
    D) None of the above
    Correct Answer: B
    ---
    """

    try:
        # ✅ Use the latest, stable Gemini 2.5 Flash model
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        # Handle empty or malformed responses gracefully
        if not response.text or "Q:" not in response.text:
            raise ValueError("Gemini returned an empty or malformed response.")

        # Split by questions
        lines = response.text.split("Q:")
        questions = []

        for line in lines:
            if not line.strip():
                continue

            text = line.strip()
            q_type = "General"
            difficulty = "Medium"

            # Extract type
            if "MCQ" in text or "mcq" in text:
                q_type = "MCQ"
            elif "Pseudocode" in text or "pseudo" in text:
                q_type = "Pseudocode"
            elif "Coding" in text or "code" in text:
                q_type = "Coding"

            # Extract difficulty
            if "Easy" in text:
                difficulty = "Easy"
            elif "Difficult" in text or "Hard" in text:
                difficulty = "Difficult"

            # Structure question object
            question = {
                "text": text.replace("Type:", "").replace("Difficulty:", "").strip(),
                "type": q_type,
                "difficulty": difficulty
            }
            questions.append(question)

        # Always limit to 10 questions
        return questions[:10]

    except Exception as e:
        print(f"⚠️ Gemini API Error: {e}")
        print("👉 Using fallback questions instead.")
        # --- Fallback hardcoded questions (in case API fails)
        fallback = [
            {"text": "What is a Python decorator? Give an example.", "type": "MCQ", "difficulty": "Medium"},
            {"text": "Write pseudocode for sorting an array using bubble sort.", "type": "Pseudocode", "difficulty": "Easy"},
            {"text": "Write code to reverse a string in Java.", "type": "Coding", "difficulty": "Medium"},
            {"text": "What is encapsulation in OOP?", "type": "MCQ", "difficulty": "Easy"},
            {"text": "Write pseudocode to find the largest of three numbers.", "type": "Pseudocode", "difficulty": "Easy"},
            {"text": "Write code to check if a number is prime in Python.", "type": "Coding", "difficulty": "Medium"},
            {"text": "What is the difference between a stack and a queue?", "type": "MCQ", "difficulty": "Medium"},
            {"text": "Write pseudocode for binary search.", "type": "Pseudocode", "difficulty": "Medium"},
            {"text": "Write code to count vowels in a string in Java.", "type": "Coding", "difficulty": "Medium"},
            {"text": "Explain polymorphism with an example.", "type": "MCQ", "difficulty": "Medium"},
        ]
        return fallback
