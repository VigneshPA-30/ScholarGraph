from langchain_core.tools import tool


class Tools:
    def __init__(self, dependecymanager):
        self.dependecymanager = dependecymanager
        # self.allTools = []


    def gettools(self):
        return self.allTools
    
    @tool
    def retrieverTool(self,query:str):
        """Retrieves top 5 docs stored in the vector database that is relevant to the given query"""

        self.docparserobj = self.dependecymanager.getdocparsingobj()
        retriever = self.docparserobj.getRetriever()
        retrievedDocs = retriever.invoke(query)
        return retrievedDocs



    