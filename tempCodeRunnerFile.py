from flask import Flask, render_template, request, jsonify, redirect, url_for
from resume_parser import extract_skills
from question_gen import generate_questions
from feedback_engine import get_feedback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')  # intro page

@app.route('/upload')
def upload_page():
    return render_template('upload.html')  # upload resume page

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    if not file:
        return jsonify({'error': 'No file uploaded'})
    skills = extract_skills(file)
    questions = generate_questions(skills)
    return render_template('interview.html', skills=skills, questions=questions)

# 🆕 Route for single "Submit All" feedback
@app.route('/feedback_all', methods=['POST'])
def feedback_all():
    answers = [v for k, v in sorted(request.form.items())]
    feedback_list = [get_feedback(a, f"Q{i+1}") for i, a in enumerate(answers)]
    return jsonify({"feedback": feedback_list})

# Old route (you can keep it for safety)
@app.route('/feedback', methods=['POST'])
def feedback():
    answer = request.json['answer']
    question = request.json['question']
    fb = get_feedback(answer, question)
    return jsonify({'feedback': fb})

if __name__ == '__main__':
    app.run(debug=True)
