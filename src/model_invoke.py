
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


class ModelInvoke:
    def __init__(self, llm_model:str="gemini-2.5-flash-lite", embedding_model:str="gemini-embedding-001"):
        self.llm_model= llm_model
        self.embedding_model = embedding_model
        self.textembeddings = GoogleGenerativeAIEmbeddings(model=self.embedding_model)
    

    def LLMModelInvoke(self):
        llm = ChatGoogleGenerativeAI(
            model=self.llm_model,
            temperature=0.3
        )

        return llm
    
    def TextembeddingModelInvoke(self):
        return self.textembeddings