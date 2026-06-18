from src.model_invoke import ModelInvoke
from src.document_loader import Embeddings
from utils.prompts import main_prompt



class Chat:
    def __init__(self):
        # self.model = ModelInvoke()
        # self.model = M.ModelInvoke()
        self.emb = Embeddings(self.model)
        self.llm = self.model.LLMModelInvoke()
        self.hash_values = []

    def retrieveDocs(self, input):
        retriever = self.emb.getRetriever(self.hash_values)
        retrievedDocs = retriever.invoke(input)
        return retrievedDocs


    def ChatwithLLM(self, input:str="Hello!", retrievedDocs:str="",use_docs:bool=True):
        # print(retrievedDocs)
        prompt = main_prompt(input, retrievedDocs)
        response = self.llm.invoke(prompt)

        return response.content


