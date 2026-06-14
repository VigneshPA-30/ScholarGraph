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
    def __init__(self,pdf_paths:list):
        self.chat = Chat()
        for path in pdf_paths:
            print(f"ChatNode: {path}")
            self.chat.load_documents(str(path))

    def retrieveDocs(self, ChatState):
        docs = self.chat.retrieveDocs(ChatState["input"])
        return {"context":docs}
    
    def ChatwithLLM(self, ChatState,usedocs:bool=True):
        answer = self.chat.ChatwithLLM(ChatState["input"], ChatState["context"], usedocs)
        return {"output":answer}
    


def builderGraph(DOC_PATHS):
    print(f"Builder Graph {DOC_PATHS}")
    nodes = ChatNode(DOC_PATHS)
    builder = StateGraph(ChatState)

    builder.add_node("retriever", nodes.retrieveDocs)
    builder.add_node("ChatwithLLM",nodes.ChatwithLLM)

    builder.add_edge(START,"retriever")
    builder.add_edge("retriever","ChatwithLLM")
    builder.add_edge("ChatwithLLM",END)

    graph = builder.compile()
    return graph






