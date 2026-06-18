from fastapi import FastAPI, Request, HTTPException, File, UploadFile as StandardUploadFile
from pydantic import BaseModel, WithJsonSchema, Field
from contextlib import asynccontextmanager
from typing import List, Annotated
from start import appStartObj
import os, shutil
from pathlib import Path



class InputText(BaseModel):
    user_input:str = Field(description="Input from User")

UploadFile = Annotated[StandardUploadFile, WithJsonSchema({"type": "string", "format": "binary"})]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading Objects...")
    app.state.Start = appStartObj()
    print("Loaded Objects...")
    yield
    print("Closing App...")

app = FastAPI(lifespan=lifespan)

UPLOAD_DIR = Path("utils/uploadedDocuments")
os.makedirs(UPLOAD_DIR, exist_ok = True)



@app.get("/")
def root():
    return{"response":"FastAPI running..."}


@app.post("/chat")
async def chat(request: Request, user_ip:InputText):
    start = request.app.state.Start
    try:
        output = start.start_chat(user_ip.user_input)
        # print(output)
        return {"response":output, "success":True}
    except Exception as e:
        raise HTTPException(status_code =500, detail=str(e))





@app.post("/upload")
async def upload_document(request: Request, files:List[UploadFile]= File(...)):
    start = request.app.state.Start
    filepaths = []

    for file in files:
        try:
            file_path = Path(UPLOAD_DIR,file.filename)
            with open(file_path,"wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            filepaths.append(file_path)
        except Exception as e:
            return {f"Error Occurred Uploading Docs as  {e}"}
        
        finally:
            file.file.close()

    flag = start.uploaded_doc_paths(filepaths)

    return flag


    


    
