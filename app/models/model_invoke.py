from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


class ModelInvoke:
    def __init__(self):
        pass


    def LLMModelInvoke(self, llm_model:str="gemini-2.5-flash-lite"):
        llm = ChatGoogleGenerativeAI(
            model=llm_model,
            temperature=0.3
        )
        return llm
    
    def textembeddingModelInvoke(self, embedding_model:str="gemini-embedding-001"):
        textembeddingsModel = GoogleGenerativeAIEmbeddings(model=embedding_model)
        return textembeddingsModel
    
    def chunkingModelInvoke(self, chunking_model:str="gemini-2.5-flash-lite"):
        chunkingModel = ChatGoogleGenerativeAI(
            model=chunking_model,
            temperature=0
        )
        return chunkingModel