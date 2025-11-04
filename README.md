# 🤖 AI Interview Coach

**AI Interview Coach** is a smart Flask-based web application that helps users prepare for interviews using AI. It analyzes resumes, generates relevant questions, and provides instant feedback — just like a real interview coach.

---

## 🚀 Features
- 🧠 AI-generated interview questions based on your resume or chosen role  
- 📄 Resume parser that extracts key skills and experience  
- 💬 Smart feedback engine to evaluate and improve answers  
- 🎨 Simple and elegant web interface built with Flask, HTML, and CSS  

---

## 🗂️ Project Structure
ai_interview_coach/
│
├── app.py                 # Main Flask application
├── resume_parser.py       # Extracts skills from uploaded resumes
├── question_gen.py        # Generates interview questions using extracted skills
├── feedback_engine.py     # Provides AI-based feedback on answers
├── requirements.txt       # Dependencies
│
├── static/                # CSS and static assets
│   └── style.css
│
└── templates/             # HTML templates
    ├── home.html          # Intro page with project info and "Next" button
    └── upload.html        # Resume upload and interview interface

---

## ⚙️ How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/navneetchinchole04/ai_interview_coach.git
   cd ai_interview_coach
2. **Install dependencies**
   pip install -r requirements.txt
3. **Run the Flask app**
   python app.py
4. **Open in browser**
   http://127.0.0.1:5000/

---

## 🚀 Future Improvements
- Add database to store user sessions and feedback  
- Enhance NLP-based skill extraction accuracy  
- Integrate AI model (like OpenAI API or Llama) for personalized interview questions  
- Deploy on Render or Hugging Face Spaces for public use  

---

## 💡 Author
Developed by **Navneet Chinchole**  
📧 navneetchinchole04@gmail.com  
🔗 [GitHub Profile](https://github.com/navneetchinchole04)

   
