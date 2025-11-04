def generate_questions(skills):
    questions = []
    for skill in skills[:5]:
        q = f"What are your key strengths in {skill}? Can you explain a real-world use case?"
        questions.append(q)
    return questions
