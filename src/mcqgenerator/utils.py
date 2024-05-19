import os
import PyPDF2
import io

def extract_text_from_file(uploaded_file):
    try:
        if uploaded_file is not None:
            file_type = uploaded_file.name.split('.')[-1].lower()

            if file_type == 'pdf':
                # Open the uploaded PDF file as a binary stream
                with io.BytesIO(uploaded_file.read()) as file:
                    # Read the PDF file using PyPDF2
                    pdf_reader = PyPDF2.PdfReader(file)
                    
                    # Initialize a variable to hold the extracted text
                    all_text = ""
                    
                    # Iterate over all the pages and concatenate the text
                    for page in pdf_reader.pages:
                        all_text += page.extract_text()
                    
                    return all_text
            
            elif file_type == 'txt':
                # Read the text file
                text = uploaded_file.read().decode('utf-8')
                return text
            
            else:
                return "Unsupported file type."
        else:
            return "No file uploaded."
    except Exception as e:
        return f"An error occurred while reading the file: {e}"
