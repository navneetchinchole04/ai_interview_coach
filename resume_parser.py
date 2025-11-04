import fitz  # PyMuPDF
import re

def extract_skills(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    # Common technical skill keywords
    skill_keywords = [
        "Python", "Java", "C", "C++", "SQL", "HTML", "CSS", "JavaScript",
        "Flask", "Django", "React", "Node", "Angular", "Spring", "Machine Learning",
        "Deep Learning", "Data Analysis", "NLP", "Pandas", "NumPy", "TensorFlow",
        "Keras", "Power BI", "Excel", "Git", "GitHub", "Tableau", "MongoDB",
        "Firebase", "Streamlit", "OpenCV", "AWS", "REST API", "JSON"
    ]

    found = []
    for skill in skill_keywords:
        # Case-insensitive search
        if re.search(rf'\b{skill}\b', text, re.IGNORECASE):
            found.append(skill)

    return sorted(list(set(found)))
