# ResuMate - AI-Powered Resume Reviewer & Job Readiness Coach

## Description
ResuMate is a Flask-based web application that allows users to upload their resumes in PDF or DOCX format. The app extracts the text from the resume, scores it based on ATS compatibility, grammar, and format, and provides AI-generated suggestions for improvement using the Gemini API.

## Features
- Upload resumes in PDF or DOCX format
- Extract resume text using PyMuPDF and python-docx
- Score resumes on ATS compatibility, grammar, and format
- AI-generated feedback and suggestions for improvement via Gemini API
- Clean, professional, and user-friendly web interface

## Folder Structure
```
resumate/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── utils/
│   ├── parser.py
│   ├── scorer.py
│   └── ai_feedback.py
├── uploads/
├── requirements.txt
└── README.md
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd resumate
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set the Gemini API key as an environment variable:
   ```
   export GEMINI_API_KEY="your_gemini_api_key_here"  # On Windows: set GEMINI_API_KEY="your_gemini_api_key_here"
   ```

## Running the App Locally
```
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to use ResuMate.

## Notes
- Ensure you have the Gemini API key to get AI feedback.
- Uploaded resumes are saved in the `uploads/` folder.
- The scoring logic is basic and can be enhanced further.

## License
MIT License
