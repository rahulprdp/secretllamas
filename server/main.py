from flask import Flask, jsonify , request
import time, requests, os
import PyPDF2

## Global
# List to store extracted text from PDFs
extracted_text_list = []
pdf_directory = 'C:/Users/Starlord/Desktop/secretllamas/pdf'

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text



def list_pdf_files(directory):
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_files.append(filename)
    return pdf_files


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/files")
def list():
    resp = list_pdf_files(pdf_directory)
    response_data = {
        "files": resp
    }

    # Create a JSON response
    response = jsonify(response_data)
    
    # Add CORS headers to the response
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")

    return response, 200

#Endpoint to prepare pdfs for the model : Convert PDFs to txt files
@app.route("/prepare")
def pepare():
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
    # Create a JSON response
    response = jsonify(response_data)
    
    # Add CORS headers to the response
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")

    return response, 200


# Function to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    response_data = {
        "message": "Something went wrong!"
    }
    # Create a JSON response
    response = jsonify(response_data)
    
    # Add CORS headers to the response
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")


    if 'file' not in request.files:
        return response, 400

    file = request.files['file']

    if file.filename == '':
        return response, 400

    if file:
        filename = file.filename
        file.save(os.path.join(pdf_directory, filename))
        response_data = {
        "message": "File uploaded sucessfully"
        }
        # Create a JSON response
        response = jsonify(response_data)
        
        # Add CORS headers to the response
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

    return response, 400



# Function to handle file uploads
@app.route('/summary', methods=['POST'])
def get_summary():
    file_name = request.args.get('file_name')

    response_data = {
        "summary": file_name
    }

    # Create a JSON response
    response = jsonify(response_data)
    
    # Add CORS headers to the response
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")


    return response, 200