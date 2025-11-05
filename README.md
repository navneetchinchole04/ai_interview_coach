# 🤖 AI Interview Coach

**AI Interview Coach** is an intelligent Flask-based web application that helps users prepare for interviews using Artificial Intelligence.  
It analyzes resumes, generates relevant questions, and provides instant feedback — just like a real interview coach!

---

## 🚀 Features

- 🧠 AI-generated interview questions based on your uploaded resume or chosen role  
- 📄 Resume parser that extracts key skills and experience automatically  
- 💬 Smart feedback engine to evaluate and improve your responses  
- ⏱️ 50-minute timer to simulate a real interview session  
- 🔐 Secure login/signup with strong password validation  
- 🎨 Glassmorphism UI with glowing buttons and smooth animations  
- 🤖 Integrated with **Google Gemini 2.5 Flash API** to generate dynamic, AI-powered interview questions securely using `.env` for key management  

---

## 🔑 Gemini API Setup

To enable AI-generated questions, this project integrates **Google Gemini 2.5 Flash API**.

1. Go to [Google AI Studio](https://aistudio.google.com/).  
2. Create a new API key under your Google Cloud project.  
3. Create a `.env` file in your main folder and add:
4. The key is securely loaded using python-dotenv in the app.

⚠️ Note: The .env file is ignored via .gitignore and never pushed to GitHub, ensuring API key security.

---

   ```bash
   GEMINI_API_KEY=your_api_key_here

## 🗂️ Project Structure
ai_interview_coach/
│
├── app.py # Main Flask application
├── resume_parser.py # Extracts skills from uploaded resumes
├── question_gen.py # Generates interview questions
├── feedback_engine.py # Provides AI-based feedback
├── requirements.txt # Dependencies
│
├── static/ # CSS and other static assets
│ └── style.css
│
└── templates/ # HTML templates
├── home.html # Homepage
├── upload.html # Resume upload & question generation
├── interview.html # Interactive interview interface
└── signup.html # Signup with validation

```
---

## ⚙️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/navneetchinchole04/ai_interview_coach.git
cd ai_interview_coach
```

### 2️⃣ Install dependencies
pip install -r requirements.txt

### 3️⃣ Run the Flask app
python app.py

### 4️⃣ Open in browser
👉 http://127.0.0.1:5000/

---

🧾 Example Flow

1. Sign up securely with password validation (min 7 chars, 1 uppercase, 1 lowercase, 1 digit).

2. Upload your resume — the system extracts your technical skills.

3. Start your AI interview — get questions (MCQs, pseudocode, coding).

4. Submit answers and receive a thank-you screen with smooth transitions.

---

🚀 Future Improvements

🗄️ Add database support (SQLite/Firebase) for persistent user data

🤖 Integrate an advanced AI model (e.g., GPT or LLaMA) for dynamic questions

🧩 Add analytics dashboard for interview performance tracking

🌐 Deploy on Render / Vercel / Hugging Face Spaces

---

## 💡 Author

**👨‍💻 Navneet Chinchole**  
🎓 B.Tech in Electronics & Computer Engineering  
📧 [navneetchinchole04@gmail.com](mailto:navneetchinchole04@gmail.com)  
🔗 [GitHub Profile](https://github.com/navneetchinchole04)

---

⭐ If you found this project useful, please give it a star on GitHub! 🌟
