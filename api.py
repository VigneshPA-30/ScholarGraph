from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from start import start_chat

app = FastAPI()

class InputText(BaseModel):
    user_input:str




@app.get("/")
def root():
    return{"response":"FastAPI running...😄"}


@app.post("/chat")
def chat(user_ip:InputText):
    try:
        output = start_chat(user_ip.user_input)
        print(output)
        return {"response":output, "success":True}
    except Exception as e:
        raise HTTPException(status_code =500, detail=str(e))
    


    
