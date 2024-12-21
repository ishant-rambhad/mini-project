from langchain.chains import ConversationalRetrievalChain
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
import os
import tempfile
from InstructorEmbedding import INSTRUCTOR

from langchain.embeddings import HuggingFaceInstructEmbeddings, SentenceTransformerEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

# Create llm
llm = LlamaCpp(
    streaming = True,
    model_path="Mistral-7B-Instruct-v0.1-GGUF\mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    temperature=0.75,
    top_p=1,
    verbose=True,
    n_ctx=4096
)

# embeddings = HuggingFaceInstructEmbeddings(
#     model_name = os.path.join(os.getcwd(), "instruct-large"),
#     model_kwargs = {"device" : "cpu"},
#     encode_kwargs = {"normalize_embeddings":True},
#     query_instruction = "Represent the query for retrieval:"
# )


embeddings = HuggingFaceEmbeddings(model_name=os.path.join(os.getcwd(),"all-MiniLM-L6-V2"))

temp_file_path = "uploaded_files\CCN____ACT1.2.pdf"
loader = PyPDFLoader(temp_file_path)
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
text_chunks = text_splitter.split_documents(data)

vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
            retriever=vector_store.as_retriever(search_kwargs={"k": 2}), memory=memory)

# query = "what this document is about?"
# query=input("enter question: ") 


# history.append((query, result["answer"]))

# result = chain("question":query, "chat_history":history)
# print(result)
history = []

def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

while True:
    query = input("Enter your question (type 'quit' to exit): ")
    if query.lower() == 'quit':
        break

    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    print(result["answer"])

print("Exiting the conversation.")
