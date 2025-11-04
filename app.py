from flask import Flask, render_template, request, jsonify
from resume_parser import extract_skills
from question_gen import generate_questions
from feedback_engine import get_feedback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    if not file:
        return jsonify({'error': 'No file uploaded'})
    skills = extract_skills(file)
    questions = generate_questions(skills)
    return jsonify({'skills': skills, 'questions': questions})

@app.route('/feedback', methods=['POST'])
def feedback():
    answer = request.json['answer']
    question = request.json['question']
    fb = get_feedback(answer, question)
    return jsonify({'feedback': fb})

if __name__ == '__main__':
    app.run(debug=True)