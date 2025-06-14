# Project: ResuMate - AI-Powered Resume Reviewer & Job Readiness Coach

# Folder Structure:
# resumate/
# ├── app.py
# ├── templates/
# │   ├── index.html
# │   └── extracted_text.html
# ├── static/
# │   └── style.css
# ├── utils/
# │   ├── parser.py
# │   ├── scorer.py
# │   └── ai_feedback.py
# ├── test_resumes/
# ├── requirements.txt
# └── README.md

from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from utils.parser import extract_text_from_resume
from utils.scorer import score_resume
from utils.ai_feedback import get_ai_feedback
import json
import threading

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_resume_async(file_path):
    resume_text = extract_text_from_resume(file_path)
    score = score_resume(resume_text)
    feedback_data = get_ai_feedback(resume_text)
    feedback = feedback_data.get("suggestions", [])
    tips = feedback_data.get("tips", [])

    temp_text_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_resume_text.txt')
    temp_score_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_score.txt')
    temp_feedback_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_feedback.txt')
    temp_tips_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_tips.txt')

    with open(temp_text_path, 'w', encoding='utf-8') as f:
        f.write(resume_text)
    with open(temp_score_path, 'w', encoding='utf-8') as f:
        json.dump(score, f)
    with open(temp_feedback_path, 'w', encoding='utf-8') as f:
        json.dump(feedback, f)
    with open(temp_tips_path, 'w', encoding='utf-8') as f:
        json.dump(tips, f)

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

            # Start async analysis thread
            thread = threading.Thread(target=analyze_resume_async, args=(file_path,))
            thread.start()

            # Redirect to analyzing page
            return redirect(url_for('uploading'))
    return render_template('index.html', score=None, feedback=None, tips=None)

@app.route('/resume_review')
def resume_review():
    temp_text_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_resume_text.txt')
    temp_score_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_score.txt')
    temp_feedback_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_feedback.txt')
    temp_tips_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_tips.txt')

    if os.path.exists(temp_text_path):
        with open(temp_text_path, 'r', encoding='utf-8') as f:
            resume_text = f.read()
    else:
        resume_text = "No extracted resume text available."

    score = {}
    feedback = []
    tips = []
    if os.path.exists(temp_score_path):
        with open(temp_score_path, 'r', encoding='utf-8') as f:
            score = json.load(f)
    if os.path.exists(temp_feedback_path):
        with open(temp_feedback_path, 'r', encoding='utf-8') as f:
            feedback = json.load(f)
    if os.path.exists(temp_tips_path):
        with open(temp_tips_path, 'r', encoding='utf-8') as f:
            tips = json.load(f)

    # Ensure all expected keys exist in score dictionary for template and convert to float if possible
    expected_keys = ['ats_raw', 'grammar_raw', 'format_raw', 'total_raw', 'ats', 'grammar', 'format', 'total']
    for key in expected_keys:
        if key not in score:
            score[key] = 0
        else:
            try:
                score[key] = float(score[key])
            except (ValueError, TypeError):
                score[key] = 0

    return render_template('resume_review.html', resume_text=resume_text, score=score, feedback=feedback, tips=tips)

@app.route('/uploading')
def uploading():
    return render_template('uploading.html')

@app.route('/analysis_status')
def analysis_status():
    temp_score_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_score.txt')
    if os.path.exists(temp_score_path):
        return {'status': 'complete', 'redirect_url': url_for('resume_review')}
    else:
        return {'status': 'processing'}

if __name__ == '__main__':
    app.run(debug=True)


