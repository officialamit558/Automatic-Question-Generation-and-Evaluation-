import PyPDF2
import docx

# File upload interface
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Parse uploaded files
def parse_uploaded_files(files):
    content = ""
    for file in files:
        if file.filename.lower().endswith('.pdf'):
            content += extract_text_from_pdf(file)
        elif file.filename.lower().endswith('.docx'):
            content += extract_text_from_docx(file)
    return content

