import os
import google.generativeai as genai
import json
import re

# Configure Gemini with API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# 🧩 Function 1 — Generate Written Questions
def generate_questions(skills):
    """
    Generates a mix of written interview questions (MCQ, coding, pseudocode)
    based on the extracted skills from the resume.
    """
    prompt = f"""
    You are an AI interview question generator.
    Based on the following technical skills: {', '.join(skills)},
    create 10 written interview questions — a mix of MCQs, pseudocode, and coding questions.
    Each question should include difficulty level tags: Easy, Medium, or Difficult.

    Format the output as:
    [
      {{
        "type": "MCQ" / "Pseudocode" / "Coding" / "Conceptual",
        "difficulty": "Easy" / "Medium" / "Difficult",
        "text": "Question text here"
      }}
    ]
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-pro")
        response = model.generate_content(prompt)
        text = response.text
        json_str = re.search(r'\[.*\]', text, re.DOTALL).group()
        questions = json.loads(json_str)
        return questions
    except Exception as e:
        print("⚠️ Error generating written questions:", e)
        return [
            {"type": "Conceptual", "difficulty": "Medium", "text": "Explain your experience with AI projects."}
        ]


# 🧩 Function 2 — Generate Video Interview Questions
def generate_video_questions(skills):
    """
    Generates 2 AI-driven video interview questions where the candidate
    must respond verbally. The questions test communication, confidence,
    and technical understanding.
    """
    prompt = f"""
    You are an AI interview coach generating video-based interview questions.
    Based on these skills: {', '.join(skills)},
    create 2 verbal interview questions that the candidate will answer on video.
    
    Each question should be clear and require a spoken explanation or reasoning.
    Also suggest a time limit (in seconds) suitable for each question.
    
    Example format:
    [
      {{
        "question": "Describe a challenging machine learning project you worked on.",
        "time_limit": 90
      }},
      {{
        "question": "Explain how REST APIs work and why they are useful.",
        "time_limit": 60
      }}
    ]
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-pro")
        response = model.generate_content(prompt)
        text = response.text
        json_str = re.search(r'\[.*\]', text, re.DOTALL).group()
        questions = json.loads(json_str)
        return questions
    except Exception as e:
        print("⚠️ Error generating video questions:", e)
        return [
            {"question": "Tell us about your most impactful technical project and your role in it.", "time_limit": 90},
            {"question": "Explain a recent technology trend that excites you and why.", "time_limit": 60}
        ]


# 🧩 Function 3 — Evaluate Video Answer using Gemini
def evaluate_video_answer(question_text, transcript_text):
    """
    Uses Gemini to evaluate the candidate’s verbal response to a question.
    Returns structured feedback with scores and a short summary.
    """
    prompt = f"""
    You are an AI interview evaluator.

    Interview Question:
    "{question_text}"

    Candidate's Transcribed Response:
    "{transcript_text}"

    Evaluate this answer on a scale of 1–10 for the following:
    1. Clarity of explanation
    2. Relevance to the question
    3. Confidence and tone
    4. Structure and logical flow
    5. Overall communication effectiveness

    Also, provide a short feedback summary (2–3 sentences) highlighting
    the candidate’s strengths and one area of improvement.

    Format your response as JSON:
    {{
      "scores": {{
        "Clarity": 8,
        "Relevance": 7,
        "Confidence": 9,
        "Structure": 8,
        "Overall": 8
      }},
      "feedback": "Strong and clear explanation. Maintain eye contact and give more examples next time."
    }}
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-pro")
        response = model.generate_content(prompt)
        text = response.text
        json_str = re.search(r'\{.*\}', text, re.DOTALL).group()
        feedback = json.loads(json_str)
        return feedback
    except Exception as e:
        print("⚠️ Error generating Gemini feedback:", e)
        return {
            "scores": {"Clarity": 7, "Relevance": 7, "Confidence": 7, "Structure": 7, "Overall": 7},
            "feedback": "Good response. Try to elaborate more and speak confidently."
        }

