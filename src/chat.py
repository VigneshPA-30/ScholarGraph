from src.model_invoke import ModelInvoke
from src.document_loader import Embeddings
from utils.prompts import main_prompt


class Chat:
    def __init__(self):
        self.model = ModelInvoke()
        # self.model = M.ModelInvoke()
        self.emb = Embeddings()
        self.llm = self.model.LLMModelInvoke()

    def load_documents(self, path):
        self.retriever = self.emb.PdfEmbeddings(self.model, path)


    def ChatwithLLM(self, input:str="Hello!", use_docs:bool=True):

        
        retrievedDocs = self.retriever.invoke(input)
        # print(retrievedDocs)

        
        prompt = main_prompt(input, retrievedDocs)
        response = self.llm.invoke(prompt)

        return response.content


