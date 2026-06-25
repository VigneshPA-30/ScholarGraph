from langchain_core.tools import tool


class Tools:
    def __init__(self, dependecymanager):
        self.dependecymanager = dependecymanager
        # self.allTools = []


    def gettools(self):
        return self.allTools
    
    def getretrieverTool(self):
        """Retrieves top 5 docs stored in the vector database that is relevant to the given query from the knowledge base"""

        @tool
        def retrieverTool(query:str):
            """Retrieves top 5 docs stored in the vector database that is relevant to the given query"""
            print("Tool called....")
            docparserobj = self.dependecymanager.getdocparsingobj()
            retriever = docparserobj.getRetriever()
            docs = retriever.invoke(query)
            if not docs:
                return "NO_RELEVANT_CONTEXT"
            return "\n\n".join([doc.page_content for doc in docs])
        
        return retrieverTool
        




    