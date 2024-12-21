from langchain.document_loaders import PyPDFLoader
import os
import tempfile
import PyPDF2


def dir_loader():
    # temp_file_path = "D:\\LLM_Project\\uploaded_files\\CCN____ACT1.2.pdf"
    # loader = PyPDFLoader(temp_file_path)
    # data = loader.load()
    directory_path = "D:/Projects/mini project/LLM_Project - Copy/uploaded_files/CCN____ACT1.2.pdf"
    pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        file_path = os.path.join(directory_path, pdf_file)
        loader = PyPDF2.PdfFileReader(file_path)
        data = loader.load()
        
        return data
    