from typing import TypedDict
from src.chat import Chat
from langgraph.graph import (
    StateGraph,
    START,
    END
)

class ChatState(TypedDict):
    input:str
    context:str
    output:str


class ChatNode():
    def __init__(self):
        self.chat = Chat()
        self.chat.load_documents(r"C:\Users\pavig\Downloads\Vignesh_PA_Resume (1).pdf")

    def retrieveDocs(self, ChatState):
        docs = self.chat.retrieveDocs(ChatState["input"])
        return {"context":docs}
    
    def ChatwithLLM(self, ChatState,usedocs:bool=True):
        answer = self.chat.ChatwithLLM(ChatState["input"], ChatState["context"], usedocs)
        return {"output":answer}
    


def builderGraph():
    nodes = ChatNode()
    builder = StateGraph(ChatState)

    builder.add_node("retriever", nodes.retrieveDocs)
    builder.add_node("ChatwithLLM",nodes.ChatwithLLM)

    builder.add_edge(START,"retriever")
    builder.add_edge("retriever","ChatwithLLM")
    builder.add_edge("ChatwithLLM",END)

    graph = builder.compile()
    return graph






