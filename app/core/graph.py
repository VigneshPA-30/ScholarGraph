from typing import TypedDict
from app.core.chat import Chat
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
    def __init__(self, docparserobj,modelinvokeobj):
        self.chat = Chat(docparserobj,modelinvokeobj)
        # for path in pdf_paths:
        #     print(f"ChatNode: {path}")
        #     self.chat.load_documents(str(path))

    def retrieveDocs(self, ChatState):
        docs = self.chat.retrieveDocs(ChatState["input"])
        return {"context":docs}
    
    def ChatwithLLM(self, ChatState,usedocs:bool=True):
        answer = self.chat.ChatwithLLM(ChatState["input"], ChatState["context"], usedocs)
        return {"output":answer}
    


def builderGraph(docparserobj,modelinvokeobj):
    # print(f"Builder Graph {DOC_PATHS}")
    nodes = ChatNode(docparserobj,modelinvokeobj)
    builder = StateGraph(ChatState)

# Building Nodes
    builder.add_node("retriever", nodes.retrieveDocs)
    builder.add_node("ChatwithLLM",nodes.ChatwithLLM)

#Connecting Nodes
    builder.add_edge(START,"retriever")
    builder.add_edge("retriever","ChatwithLLM")
    builder.add_edge("ChatwithLLM",END)

    graph = builder.compile()
    return graph






