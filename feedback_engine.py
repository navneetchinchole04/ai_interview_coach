def get_feedback(answer, question):
    if len(answer.split()) < 20:
        return "Your answer is too short. Try explaining more details and examples."
    elif "project" in answer.lower():
        return "Good — you gave a project-based answer! You could also add impact or metrics."
    else:
        return "Answer looks fine. Try adding practical examples to improve it."
