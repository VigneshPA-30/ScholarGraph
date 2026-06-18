# from src.chat import Chat
from src.graph import builderGraph
from src.chat import Chat
from src.model_invoke import ModelInvoke
from src.model_invoke import DocumentProcessor
from typing import List


class Start():
    def __init__(self):
        self.modelinvoke = ModelInvoke()
        self.docprocessing = DocumentProcessor(self.modelinvoke)

    def uploaded_doc_paths(self,pdf_paths:List):
        return self.docprocessing.startprocessing(pdf_paths)

    def start_chat(self, user_ip:str):
        # print(f"Doc paths in BuilderGraph call : {self.DOC_PATHS}")
        graph = builderGraph()
        
        answer = graph.invoke({
                "input": user_ip,
                "context": "",
                "output": ""
            })
        print(answer["output"])
        return answer["output"]
    


def appStartObj():
    return Start()

def main():
    #dummy for local test
    print("Starting from inside SRC folder") #for dev

    Start.start_chat("What is my name?")

    

   

# if __name__ == "__main__":
#     main()
