import PyPDF2

def extract_text_by_paragraph(pdf_path):
    paragraphs = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                page_paragraphs = text.split('\n\n')
                paragraphs.extend(page_paragraphs)
    
    return paragraphs