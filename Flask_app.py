from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import LlamaCpp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
import os

app = Flask(__name__)
CORS(app)


def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

# Initialize LangChain components
llm = LlamaCpp(
    streaming=True,
    model_path="D:\\Projects\\mini project\\LLM_Project - Copy\\Mistral-7B-Instruct-v0.1-GGUF\\mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    temperature=0.75,
    top_p=1,
    verbose=True,
    n_ctx=4096
)
print("1")
embeddings = HuggingFaceEmbeddings(model_name=os.path.join(os.getcwd(),"all-MiniLM-L6-V2"))
print("2")
# This line needs to be updated with the actual path to your PDF file
temp_file_path = "D:\\Projects\\mini project\\LLM_Project - Copy\\uploaded_files\\CCN____ACT1.2.pdf"
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

@app.route('/')
def index():
    return render_template('demo.html')

@app.route('/conversation', methods=['POST'])
def conversation():
    if request.method == 'POST':
        print("hello")
        data = request.get_json()  # Parse JSON data from request body
        query = data['question']
        history = data.get('chat_history', [])
        result = conversation_chat(query, chain, history)
        print(result)
        return jsonify(result)  # Return JSON response


if __name__ == '__main__':
    app.run(port=5012, debug=True)
