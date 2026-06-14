# from src.chat import Chat
from src.graph import builderGraph
from src.chat import Chat

DOC_PATHS = []
def uploaded_doc_paths(pdf_path):
    DOC_PATHS.append(pdf_path)



def start_chat(user_ip:str):
    print("Starting from inside SRC folder") #for dev
    print(f"Doc paths in BuilderGraph call : {DOC_PATHS}")
    graph = builderGraph(DOC_PATHS)
    
    answer = graph.invoke({
            "input": user_ip,
            "context": "",
            "output": ""
        })
    print(answer["output"])
    return answer["output"]

def main():
    start_chat("What is my name?")

    

   

# if __name__ == "__main__":
#     main()
