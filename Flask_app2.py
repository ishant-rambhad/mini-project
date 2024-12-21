from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import LlamaCpp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
import json
import os

app = Flask(__name__)
CORS(app)

chain = None  # Define chain globally

def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def LLM():
    global chain  # Use the global chain variable
    # Initialize LangChain components
    llm = LlamaCpp(
        streaming=True,
        model_path="D:\\Projects\\mini project\\LLM_Project - Copy\\Mistral-7B-Instruct-v0.1-GGUF\\mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        temperature=0.75,
        top_p=1,
        verbose=True,
        n_ctx=4096
    )
    # print("1")
    embeddings = HuggingFaceEmbeddings(model_name=os.path.join(os.getcwd(),"all-MiniLM-L6-V2"))
    # print("2")
    # This line needs to be updated with the actual path to your PDF file
    temp_file_path = "D:\\Projects\\mini project\\LLM_Project - Copy\\uploaded_files\\LLM.pdf"
    loader = PyPDFLoader(temp_file_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(data)

    vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type='stuff',
        retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
        memory=memory
    )

def load_login_data():
    with open('data/login_data.json', 'r') as f:
        return json.load(f)

# Save login data to JSON file
def save_login_data(data):
    with open('data/login_data.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('text.html')

@app.route('/signup', methods=['POST'])
def signup():
    login_data = load_login_data()
    new_user = {
        'name': request.form['name'],
        'email': request.form['email'],
        'password': request.form['password']
    }
    login_data.append(new_user)
    save_login_data(login_data)
    return 'Sign up successful'

@app.route('/signin', methods=['POST'])
def signin():
    login_data = load_login_data()
    email = request.form['email']
    password = request.form['password']
    for user in login_data:
        if user['email'] == email and user['password'] == password:
            return redirect('/uploadfile')
    return 'Invalid email or password'

@app.route('/uploadfile')
def uploadfile():
    return render_template('fileupload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file provided'), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(error='No file selected'), 400

    # Save the uploaded file to the desired location
    file.save('D:/Projects/mini project/LLM_Project - Copy/uploaded_files/LLM.pdf')  # Update the path where you want to save the file
    LLM()  
    print('l1')# Initialize LangChain components
    return redirect("/InsideIQ")  # Redirect to the demo page after successful upload

@app.route('/InsideIQ')
def InsideIQ():
    print('d1')
    return render_template('demo.html')

@app.route('/conversation', methods=['POST'])
def conversation():
    LLM()
    if request.method == 'POST':
        data = request.get_json()  # Parse JSON data from request body
        query = data['question']
        history = data.get('chat_history', [])
        result = conversation_chat(query, chain, history)
        print(result)
        return jsonify(result)  # Return JSON response

if __name__ == '__main__':
    app.run(port=5012, debug=True)
