
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS

from models.llm import llm
from models.embedding import embeddings


def query_solver(data):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(data)

    vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                retriever=vector_store.as_retriever(search_kwargs={"k": 2}), memory=memory)
    
    return chain

def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]