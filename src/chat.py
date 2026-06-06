from model_invoke import ModelInvoke
from document_loader import Embeddings


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

        prompt = f"""
            Answer properly

            user_input:{input}
            context(if empty, ignore it):{retrievedDocs}
            """

        response = self.llm.invoke(prompt)

        return response.content


