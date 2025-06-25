import fitz  # PyMuPDF
from docx import Document

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyMuPDF."""
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file using python-docx."""
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\\n'.join(full_text)

def extract_text_from_resume(file_path):
    """Extract text from resume file based on extension."""
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return ""

