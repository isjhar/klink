import PyPDF2
from domain.repositories.pdfreader import PdfReader


class PyPdfReader(PdfReader):
    def read(self, file_name) -> str:
        pdf_file = open(file_name, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text = text + page.extract_text()
        return text
