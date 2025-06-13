# Project: ResuMate - AI-Powered Resume Reviewer & Job Readiness Coach

# Folder Structure:
# resumate/
# ├── app.py
# ├── templates/
# │   └── index.html
# ├── static/
# │   └── style.css
# ├── utils/
# │   ├── parser.py
# │   ├── scorer.py
# │   └── ai_feedback.py
# ├── test_resumes/
# ├── requirements.txt
# └── README.md

# ================= app.py =================
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from utils.parser import extract_text_from_resume
from utils.scorer import score_resume
from utils.ai_feedback import get_ai_feedback

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return 'No file part'
        file = request.files['resume']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            resume_text = extract_text_from_resume(file_path)
            score = score_resume(resume_text)
            feedback_data = get_ai_feedback(resume_text)
            feedback = feedback_data.get("suggestions", [])
            tips = feedback_data.get("tips", [])

            return render_template('index.html', resume_text=resume_text, score=score, feedback=feedback, tips=tips)
    return render_template('index.html', resume_text=None, score=None, feedback=None, tips=None)

if __name__ == '__main__':
    app.run(debug=True)
