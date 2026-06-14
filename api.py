from fastapi import FastAPI, HTTPException, File, UploadFile as StandardUploadFile
from pydantic import BaseModel, WithJsonSchema
from typing import List, Annotated
from start import start_chat, uploaded_doc_paths
import os, shutil
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = Path("utils/uploadedDocuments")
os.makedirs(UPLOAD_DIR, exist_ok = True)

class InputText(BaseModel):
    user_input:str

UploadFile = Annotated[StandardUploadFile, WithJsonSchema({"type": "string", "format": "binary"})]


@app.get("/")
def root():
    return{"response":"FastAPI running..."}


@app.post("/chat")
async def chat(user_ip:InputText):
    try:
        output = start_chat(user_ip.user_input)
        # print(output)
        return {"response":output, "success":True}
    except Exception as e:
        raise HTTPException(status_code =500, detail=str(e))





@app.post("/upload")
async def upload_document(files:List[UploadFile]= File(...)):
    for file in files:
        try:
            file_path = Path(UPLOAD_DIR,file.filename)
            with open(file_path,"wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            uploaded_doc_paths(file_path)        

        except Exception as e:
            return {f"Error Occurred Uploading Docs as  {e}"}
        

        finally:
            file.file.close()

    return {f"Saved files...":"files saved"}


    


    
