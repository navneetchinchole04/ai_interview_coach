import random

def generate_questions(skills):
    questions = []

    # --- 3 MCQs ---
    mcq_questions = [
        {"text": "Which of the following is not supervised learning? A) Regression B) Clustering C) Decision Tree D) Naive Bayes", "type": "MCQ", "difficulty": "Medium"},
        {"text": "Which function is called automatically when object is created? A) Constructor B) Destructor C) Overloader D) None", "type": "MCQ", "difficulty": "Medium"},
        {"text": "Which keyword is used to create a class in Python? A) object B) define C) class D) create", "type": "MCQ", "difficulty": "Medium"}
    ]

    # --- 5 Pseudocode Questions ---
    pseudocode_questions = [
        {"text": "Write a pseudocode to find the largest of three numbers.", "type": "Pseudocode", "difficulty": "Medium"},
        {"text": "Write a pseudocode to check whether a number is prime.", "type": "Pseudocode", "difficulty": "Medium"},
        {"text": "Write a pseudocode to calculate factorial of a number.", "type": "Pseudocode", "difficulty": "Medium"},
        {"text": "Write a pseudocode to reverse a string.", "type": "Pseudocode", "difficulty": "Medium"},
        {"text": "Write a pseudocode to sort an array using bubble sort.", "type": "Pseudocode", "difficulty": "Medium"}
    ]

    # --- 2 Coding Questions ---
    coding_questions = [
        {"text": "Write a Python function to check if a given string is a palindrome.", "type": "Coding", "difficulty": "Difficult"},
        {"text": "Write a Python program to find the second largest number in a list.", "type": "Coding", "difficulty": "Difficult"}
    ]

    # Combine all
    questions.extend(mcq_questions)
    questions.extend(pseudocode_questions)
    questions.extend(coding_questions)

    random.shuffle(questions)  # To make it look random
    return questions
