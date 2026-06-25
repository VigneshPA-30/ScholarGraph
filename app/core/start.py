# from src.chat import Chat
from .graph import builderGraph
from .chat import Chat
from .dependencies import DependencyManager
from ..models.model_invoke import ModelInvoke
from ..tools.tools import Tools
from .callbacks import QueueStreamCallback
from .document_loader import DocumentProcessor
from typing import List
from ..orchestration.graph import MainAgentGraph
import threading
from queue import Queue


class Start():
    def __init__(self):
        self.modelinvoke = ModelInvoke()
        self.dependecymanager = DependencyManager(self.modelinvoke)

        self.docprocessing = DocumentProcessor(self.modelinvoke)
        self.tools = Tools(self.dependecymanager)
        
        self.dependecymanager.setdocparssingobj(self.docprocessing)
        self.dependecymanager.settoolsobj(self.tools)


    def uploaded_doc_paths(self,pdf_paths:List):
        return self.docprocessing.startprocessing(pdf_paths)

    def start_chat(self, user_ip:str):
        print(f"start_chat...")
        streamqueue = Queue()
        agent_graph = MainAgentGraph(self.dependecymanager)
        graph = agent_graph.mainAgentGraph()
        
        def start_graph():
            answer = graph.invoke({
                    "input": user_ip,
                    "context": [""],
                    "output": ""
                },
                config= {"callbacks":[QueueStreamCallback(streamqueue)]}
                )
            print(answer["output"])
            return answer["output"]
        
        # threading.Thread(target=start_graph).start()

        while True:
            token = streamqueue.get()
            if token is None:
                break
            yield token
    


def appStartObj():
    return Start()

def main():
    #dummy for local test
    print("Starting from inside SRC folder") #for dev

    Start.start_chat("What is my name?")

    

   

# if __name__ == "__main__":
#     main()
