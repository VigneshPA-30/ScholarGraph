import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class ModelInvoke:
    def __init__(self, model_name:str="gemini-2.5-flash-lite"):
        self.model_name = model_name
    

    def ModelInvoke(self):
        llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=0.3
        )

        return llm





class Chat:
    def __init__(self):
        M  = ModelInvoke()
        self.llm = M.ModelInvoke()

    def ChatwithLLM(self, input:str="Hello!", ):
        response = self.llm.invoke(input)
        return response.content


