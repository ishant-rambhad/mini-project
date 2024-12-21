from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

import os

from doc_loader import dir_loader
from query_engine import query_solver, conversation_chat

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

UPLOAD_FOLDER = 'uploaded_files' # The folder where uploaded files will be saved 
ALLOWED_EXTENSIONS = {'pdf'} # Define the allowed file extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file[]' not in request.files:
        return jsonify({"error": "No file part"})

    files = request.files.getlist('file[]')

    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename) 
        if os.path.isfile(file_path):
            os.remove(file_path)

    for file in files:
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

    return jsonify({"message": "File(s) uploaded successfully"})

@app.route('/process_question', methods=['POST']) 
def answer():
    try:
        if request.is_json:
            question = request.json.get('question')

            # documents = dir_loader()
            # query_engine = query_maker(documents)
            # print("starting squery engine")

            data = dir_loader()
            print("Data is Loading")
            chain = query_solver(data)
            print("Chain has Loaded")

            history = []
            ans = conversation_chat(question, chain, history)

            # ans = str(query_engine.query(question))
            # print(ans)

            return jsonify({'answer': ans})

        else:
            return jsonify({'answer': "Some exception occurred!!"})
        
    except Exception as e:
        print(f"Error, {e} occurred")
        error_occurred = {"response" : str(f'Error: {e}, occurred')}
        print(error_occurred)
        return jsonify({'answer':"Oops! some exception occurred."})

if __name__ == '__main__':
    app.run(port=5012, debug=True)