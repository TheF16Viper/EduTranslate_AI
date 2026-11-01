import fitz  # PyMuPDF
from docx import Document
from pptx import Presentation

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text() + "\n--- PAGE SEPARATOR ---\n"
    return text.strip()

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(text).strip()

def extract_text_from_pptx(file_path):
    prs = Presentation(file_path)
    text = []
    for idx, slide in enumerate(prs.slides):
        text.append(f"--- SLIDE {idx+1} ---")
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                text.append(shape.text)
    return "\n".join(text).strip()

def parse_course_material(file_path, file_extension):
    ext = file_extension.lower().replace(".", "")
    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext in ["docx", "doc"]:
        return extract_text_from_docx(file_path)
    elif ext in ["pptx", "ppt"]:
        return extract_text_from_pptx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
