from src.chat import Chat
from src.graph import builderGraph

def main():
   print("Starting from inside SRC folder") #for dev
   graph = builderGraph()
   answer = graph.invoke({
        "input": "What is my name?",
        "context": "",
        "output": ""
    })
   print(answer["output"])
    

   

if __name__ == "__main__":
    main()
