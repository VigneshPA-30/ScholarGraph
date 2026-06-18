from src.model_invoke import ModelInvoke
from src.document_loader import DocumentProcessor
from utils.prompts import main_prompt



class Chat:
    def __init__(self):
        pass

    def retrieveDocs(self):
        retriever = DocumentProcessor.getRetriever()
        retrievedDocs = retriever.invoke(input)
        return retrievedDocs


    def ChatwithLLM(self, input:str="Hello!", retrievedDocs:str="",use_docs:bool=True):
        # print(retrievedDocs)
        prompt = main_prompt(input, retrievedDocs)
        response = self.llm.invoke(prompt)

        return response.content


