# -*- coding: utf-8 -*-
import os
import google.generativeai as genai
import json
import re
import time
import traceback

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def clean_json_output(text: str):
    """Cleans and extracts a valid JSON list from Gemini output."""
    text = text.replace("```json", "").replace("```", "").replace("“", '"').replace("”", '"')
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("⚠️ Retrying JSON fix...")
            json_str = re.sub(r",\s*]", "]", json_str)
            return json.loads(json_str)
    return None

# 🧩 1. Generate 10 Written Questions
def generate_questions(skills):
    """Generates exactly 10 written interview questions using Gemini AI."""
    prompt = f"""
    You are an AI interview question generator.
    Based on these skills: {', '.join(skills)},
    generate exactly 10 interview questions as a JSON array.
    
    The split should be:
    - 3 MCQ
    - 3 Coding
    - 2 Pseudocode
    - 2 Conceptual

    Each object must strictly follow:
    {{
      "type": "MCQ" / "Coding" / "Pseudocode" / "Conceptual",
      "difficulty": "Easy" / "Medium" / "Difficult",
      "text": "Question text here"
    }}

    ⚠️ Return ONLY a valid JSON list. No explanations, no markdown, no comments.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(
            f"""
            You are a strict JSON generator.
            Output only a valid JSON array containing exactly 10 questions.
            Never cut off the last element or leave trailing commas.
            If the answer is too long, shorten questions instead of truncating JSON.
            {prompt}
            """,
            generation_config={"temperature": 0.3, "max_output_tokens": 5000}
        )

        print("\n🧠 GEMINI RAW RESPONSE START\n", response, "\n🧠 GEMINI RAW RESPONSE END\n")

        # ✅ Extract text properly
        raw_output = ""
        try:
            raw_output = response.candidates[0].content.parts[0].text.strip()
        except:
            raw_output = getattr(response, "text", "").strip()

        print("\n📜 Gemini Text Output:\n", raw_output[:1200], "\n")
        questions = clean_json_output(raw_output)
        if not questions:
            raise ValueError("Invalid JSON from Gemini")

        # Enforce 10 results
        if len(questions) < 10:
            print(f"⚠️ Gemini returned {len(questions)} questions. Adding fallback.")
            for i in range(10 - len(questions)):
                questions.append({
                    "type": "Conceptual",
                    "difficulty": "Medium",
                    "text": f"Explain your understanding of {skills[i % len(skills)]}."
                })
        elif len(questions) > 10:
            questions = questions[:10]

        return questions

    except Exception as e:
        print("❌ Gemini generation failed:", e)
        return [
            {"type": "Conceptual", "difficulty": "Medium", "text": f"What are REST APIs?"},
            {"type": "Coding", "difficulty": "Medium", "text": "Write a Python program to check if a string is a palindrome."},
            {"type": "MCQ", "difficulty": "Easy", "text": "Which data structure uses FIFO order?"},
            {"type": "Conceptual", "difficulty": "Medium", "text": "Explain OOPs concept in simple words."},
            {"type": "Pseudocode", "difficulty": "Medium", "text": "Write pseudocode for binary search."},
            {"type": "MCQ", "difficulty": "Medium", "text": "Which HTTP method is used for partial updates?"},
            {"type": "Coding", "difficulty": "Difficult", "text": "Write a Python program to detect prime numbers up to N."},
            {"type": "Conceptual", "difficulty": "Medium", "text": "Differentiate between TCP and UDP."},
            {"type": "Pseudocode", "difficulty": "Easy", "text": "Write pseudocode to find factorial of a number."},
            {"type": "MCQ", "difficulty": "Medium", "text": "Which of the following languages is dynamically typed?"}
        ]

# 🧩 2. Video Questions
def generate_video_questions(skills):
    """Generate 2 spoken interview questions."""
    prompt = f"""
    Based on these skills: {', '.join(skills)},
    generate 2 spoken video interview questions in JSON format.

    Format:
    [
      {{"question": "Question text", "time_limit": 90}},
      {{"question": "Question text", "time_limit": 60}}
    ]

    Return only valid JSON.
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "")
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("Invalid JSON for video questions.")
    except Exception as e:
        print("⚠️ Error generating video questions:", e)
        return [
            {"question": "Describe a project where you faced challenges and how you solved them.", "time_limit": 90},
            {"question": "Explain one of your favorite technologies and why it interests you.", "time_limit": 60}
        ]

# 🧩 3. Evaluate Video Response
def evaluate_video_answer(question_text, transcript_text):
    """Evaluates candidate’s verbal response using Gemini 2.5-Pro, auto-switches to 2.5-Flash when Pro fails."""

    if not transcript_text.strip():
        return {
            "scores": {"Clarity": 0, "Relevance": 0, "Confidence": 0, "Structure": 0, "Overall": 0},
            "feedback": "No speech detected. Please record your answer clearly."
        }

    prompt = f"""
    You are an AI interview evaluator.

    Interview Question:
    "{question_text}"

    Candidate's Response:
    "{transcript_text}"

    Evaluate the answer on a scale of 1–10 for:
      - Clarity of explanation
      - Relevance to the question
      - Confidence and tone
      - Structure and logical flow
      - Overall communication effectiveness

    Provide a brief, specific feedback summary.

    Respond only with valid JSON:
    {{
      "scores": {{
        "Clarity": <int>,
        "Relevance": <int>,
        "Confidence": <int>,
        "Structure": <int>,
        "Overall": <int>
      }},
      "feedback": "<2–3 lines of constructive feedback>"
    }}
    """

    def get_feedback(model_name):
        """Safely gets feedback from Gemini and ensures valid JSON response."""
        model = genai.GenerativeModel(model_name)
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.5,
                    "max_output_tokens": 500,
                    "response_mime_type": "application/json"
                }
            )
        except Exception as api_err:
            print(f"⚠️ Gemini API error on {model_name}: {api_err}")
            raise

        raw_output = ""
        try:
            if hasattr(response, "candidates") and response.candidates:
                parts = response.candidates[0].content.parts
                if parts and hasattr(parts[0], "text"):
                    raw_output = parts[0].text.strip()
                else:
                    raw_output = str(response.candidates[0].content or "")
            else:
                raw_output = getattr(response, "text", "") or ""
        except Exception as extract_err:
            print("⚠️ Extraction fallback:", extract_err)
            raw_output = str(response)

        print(f"\n🧠 GEMINI ({model_name}) RAW OUTPUT:\n{raw_output[:400]}\n")

        # 🚫 Handle empty or meaningless responses
        if not raw_output.strip() or raw_output.strip().lower() in ["{}", "role: \"model\"", "null"]:
            raise ValueError(f"{model_name} returned an empty or invalid response")

        # 🧹 Clean and extract JSON block
        raw_output = raw_output.replace("“", '"').replace("”", '"')
        match = re.search(r"\{.*\}", raw_output, re.DOTALL)
        if not match:
            raise ValueError(f"{model_name} did not return valid JSON format")

        json_text = match.group(0)
        try:
            result = json.loads(json_text)
            print(f"✅ Feedback generated using {model_name}")
            return result
        except json.JSONDecodeError as e:
            print("⚠️ JSON Decode Error — attempting auto-fix:", e)
            json_text = re.sub(r",\s*}", "}", json_text)
            json_text = re.sub(r",\s*]", "]", json_text)
            return json.loads(json_text)

    # 🚀 Try Gemini 2.5-Pro first
    try:
        return get_feedback("gemini-2.5-pro")

    except Exception as e:
        err_str = str(e).lower()

        # 🔁 Instant switch to gemini-2.5-flash on quota/invalid/empty response
        if any(term in err_str for term in ["429", "quota", "limit", "rate", "overloaded", "unavailable", "timeout", "empty", "invalid"]):
            print("⚡ gemini-2.5-pro unavailable or invalid — switching automatically to gemini-2.5-flash...")
            try:
                return get_feedback("gemini-2.5-flash")
            except Exception as flash_err:
                print("⚠️ Flash model also failed:", flash_err)
        else:
            print("⚠️ Gemini evaluation error:", e)
            traceback.print_exc()

    # 🛡️ Safe fallback
    return {
        "scores": {"Clarity": 7, "Relevance": 7, "Confidence": 7, "Structure": 7, "Overall": 7},
        "feedback": "Response detected, but Gemini servers were busy. Try again later or provide more detailed answers."
    }
