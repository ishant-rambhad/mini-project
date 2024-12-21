
from InstructorEmbedding import INSTRUCTOR

from langchain.embeddings import HuggingFaceInstructEmbeddings, SentenceTransformerEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
import os



embeddings = HuggingFaceEmbeddings(model_name=os.path.join(os.getcwd(),"all-MiniLM-L6-V2"))
# embeddings = HuggingFaceEmbeddings(model_name="D:\\Projects\\mini project\\LLM_Project - Copy\\Mistral-7B-Instruct-v0.1-GGUF\\mistral-7b-instruct-v0.1.Q4_K_M.gguf")
