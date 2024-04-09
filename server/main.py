from flask import Flask, jsonify
import time, requests, os
import PyPDF2

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# List to store extracted text from PDFs
extracted_text_list = []



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#Endpoint to prepare pdfs for the model : Convert PDFs to txt files
@app.route("/prepare")
def pepare():

    pdf_directory = 'C:/Users/Starlord/Desktop/secretllamas/pdf'

    files = []

    # Check if the directory exists
    if os.path.isdir(pdf_directory):
        # Get the list of files in the directory
        for filename in os.listdir(pdf_directory):
            if filename.endswith('.pdf'):
                # Construct the full file path
                file_path = os.path.join(pdf_directory, filename)
                # Open the file in binary mode
                with open(file_path, 'rb') as file:
                    value = (filename, file)
                    files.append({'pdf': value})
    else:
        print(f"The directory '{pdf_directory}' does not exist.")

    # Check if the directory exists
    if os.path.isdir(pdf_directory):
        # Get the list of files in the directory
        for filename in os.listdir(pdf_directory):
            if filename.endswith('.pdf'):
                # Construct the full file path
                file_path = os.path.join(pdf_directory, filename)
                
                txt_file_path = os.path.join(pdf_directory, os.path.splitext(filename)[0] + '.txt')
                                            
                # Open the PDF file in binary mode
                with open(file_path, 'rb') as pdf_file:
                    # Extract text from the PDF file
                    text = extract_text_from_pdf(pdf_file)
                    # Append extracted text to the list
                    extracted_text_list.append({'filename': filename, 'text': text})
                    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text)
    else:
        print(f"The directory '{pdf_directory}' does not exist.")

    # Get the list of items in the directory
    items = os.listdir(pdf_directory)

    # Join the items into a single string separated by a newline character
    items_string = ' , '.join(items)

    response_data = {
        "message": items_string
    }

    return jsonify(response_data), 200