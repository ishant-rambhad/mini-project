from langchain.llms import LlamaCpp

llm = LlamaCpp(
    streaming = True,
    model_path="D:\\Projects\\mini project\\LLM_Project - Copy\\Mistral-7B-Instruct-v0.1-GGUF\\mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    temperature=0.75,
    top_p=1,
    verbose=True,
    n_ctx=4096
)