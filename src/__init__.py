from chat import Chat

def main():
   print("Starting from inside SRC folder") #for dev
   chat = Chat()
   chat.load_documents(r"C:\Users\pavig\Downloads\Vignesh_PA_Resume (1).pdf")
   print(chat.ChatwithLLM("say my name"))


if __name__ == "__main__":
    main()
