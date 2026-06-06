from chat import Chat

def main():
   print("Starting from inside SRC folder") #for dev
   chat = Chat()
   print(chat.ChatwithLLM("Describe ML in 10 words"))


if __name__ == "__main__":
    main()
