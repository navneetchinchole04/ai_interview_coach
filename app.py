from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from resume_parser import extract_skills
from question_gen import generate_questions, generate_video_questions, evaluate_video_answer
from feedback_engine import get_feedback

# 🧠 Load environment variables and configure Gemini AI
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load .env file (contains your GEMINI_API_KEY)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Temporary in-memory database (use SQLite or Firebase later)
users = {}

# 🏠 Home
@app.route('/')
def home():
    return render_template('home.html')

# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user'] = username
            flash('✅ Login successful!', 'success')
            return redirect(url_for('upload_page'))
        else:
            flash('⚠️ Invalid username or password. Try again.', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

# 📝 Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('⚠️ Passwords do not match.', 'danger')
            return render_template('signup.html')

        import re
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{7,}$', password):
            flash('⚠️ Password must be 7+ chars, with upper, lower, and digit.', 'warning')
            return render_template('signup.html')

        if username in users:
            flash('⚠️ Username already exists. Try another.', 'warning')
        else:
            users[username] = password
            flash('✅ Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# 📤 Upload Page
@app.route('/upload')
def upload_page():
    if 'user' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    return render_template('upload.html')

# 📎 Upload Resume
@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'user' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    file = request.files.get('resume')
    if not file:
        flash('⚠️ No file uploaded!', 'danger')
        return redirect(url_for('upload_page'))

    skills = extract_skills(file)
    questions = generate_questions(skills)
    return render_template('interview.html', skills=skills, questions=questions)

# 💬 Written Feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    answer = request.json.get('answer')
    question = request.json.get('question')
    fb = get_feedback(answer, question)
    return jsonify({'feedback': fb})

# 🎥 Video Upload Route
@app.route('/upload_video', methods=['POST'])
def upload_video():
    video = request.files.get('video')
    if not video:
        return jsonify({'status': 'error', 'message': 'No video received'})

    os.makedirs('uploads', exist_ok=True)
    video_path = os.path.join('uploads', video.filename)
    video.save(video_path)

    print(f"🎬 Video saved successfully at: {video_path}")
    return jsonify({'status': 'success', 'path': video_path})

# 🎯 Video Round Route
@app.route('/video_round')
def video_round():
    if 'user' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    skills = ["Communication", "Problem Solving", "Confidence"]  # default fallback
    video_questions = generate_video_questions(skills)

    return render_template('video_round.html', questions=video_questions)

# 🏁 Thank You Page
@app.route('/thankyou')
def thankyou():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('thankyou.html')

# 🤖 Evaluate Video Response with Gemini
@app.route("/evaluate_response", methods=["POST"])
def evaluate_response():
    try:
        data = request.get_json()
        question_text = data.get("question")
        transcript_text = data.get("transcript")

        feedback = evaluate_video_answer(question_text, transcript_text)
        return jsonify({"status": "success", "feedback": feedback})
    except Exception as e:
        print("⚠️ Error in /evaluate_response:", e)
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
