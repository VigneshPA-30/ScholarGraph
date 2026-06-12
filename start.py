# from src.chat import Chat
from src.graph import builderGraph



def start_chat(user_ip:str):
    print("Starting from inside SRC folder") #for dev
    graph = builderGraph()
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
