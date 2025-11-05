from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from resume_parser import extract_skills
from question_gen import generate_questions
from feedback_engine import get_feedback

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Temporary in-memory database (use SQLite or Firebase later)
users = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ✅ Validate login
        if username in users and users[username] == password:
            session['user'] = username
            flash('✅ Login successful!', 'success')
            return redirect(url_for('upload_page'))
        else:
            flash('⚠️ Invalid username or password. Try again.', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')

        # ✅ Check if passwords match
        if password != confirm_password:
            flash('⚠️ Passwords do not match. Please try again.', 'danger')
            return render_template('signup.html')

        # ✅ Optional backend-level password strength validation
        import re
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{7,}$', password):
            flash('⚠️ Password must be at least 7 characters long, with one uppercase, one lowercase, and one digit.', 'warning')
            return render_template('signup.html')

        # ✅ Check if username already exists
        if username in users:
            flash('⚠️ Username already exists. Try another one.', 'warning')
        else:
            users[username] = password
            flash('✅ Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/upload')
def upload_page():
    if 'user' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'user' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    file = request.files['resume']
    if not file:
        return jsonify({'error': 'No file uploaded'})

    skills = extract_skills(file)
    questions = generate_questions(skills)
    return render_template('interview.html', skills=skills, questions=questions)

@app.route('/feedback', methods=['POST'])
def feedback():
    answer = request.json['answer']
    question = request.json['question']
    fb = get_feedback(answer, question)
    return jsonify({'feedback': fb})

if __name__ == '__main__':
    app.run(debug=True)
