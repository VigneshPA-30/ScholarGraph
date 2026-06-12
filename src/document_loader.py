from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import hashlib, json
from pathlib import Path


PROCESSED_JSON_PATH = "utils/processedfiles.json"



class DocumentLoader:
    def __init__(self):
        pass

    def PdfLoader(self, pdfpath):
        # print(pdfpath)
        loader = PyPDFLoader(pdfpath)
        docs = loader.load()
        return docs
    
    def storeHash(self,hash_value,pdfpath):
        processed_json = Path(PROCESSED_JSON_PATH)
        # hash_value = self.getHash(pdfpath)
        # new_data = {hash:pdfpath}

        if not processed_json.exists():
            jsondata = {}
        else:
            file_content = processed_json.read_text(encoding="utf-8")
            if file_content.strip():
                jsondata = json.loads(file_content)
            else:
                jsondata = {}


        jsondata[hash_value]=pdfpath
        new_content = json.dumps(jsondata)
        processed_json.write_text(new_content, encoding="utf-8")

    def isProcessed(self,pdfpath):

        processed_json = Path(PROCESSED_JSON_PATH)
        hash = self.getHash(pdfpath)

        if processed_json.exists():
            file_content = processed_json.read_text(encoding="utf-8")

            if not file_content.strip():
                return False
            
            jsondata = json.loads(file_content)
            return hash in jsondata

            
        return False  


    
    def getHash(self, pdfpath):
        hasher = hashlib.sha256()

        with open(pdfpath, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)

        return hasher.hexdigest()


class Embeddings:
    def __init__(self, model):
        self.docLoader = DocumentLoader()
        self.embeddings = model.TextembeddingModelInvoke()

    def PdfEmbeddings(self, pdfpath):
        
        hash_value = self.docLoader.getHash(pdfpath)

        if not self.docLoader.isProcessed(pdfpath):

            docs = self.docLoader.PdfLoader(pdfpath)
            for doc in docs:
                doc.metadata["pdf_hash"] = hash_value
                # print("DOC",doc)

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(docs)  

            # print("LENCHUNKS",len(chunks))      

            vector_db = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=f"./db"
            )
            self.docLoader.storeHash(hash_value,pdfpath)
        
           

        return hash_value

    def getRetriever(self, selectedHashes:list=None):
        search_kwargs = {"k":5}
        # print(selectedHashes)
        if selectedHashes:
            search_kwargs["filter"]={
                "pdf_hash":{
                "$in":selectedHashes
                }
            }

        vector_db = Chroma(
                persist_directory=f"./db",
                embedding_function=self.embeddings
            )
        

        return vector_db.as_retriever(
                search_kwargs= search_kwargs
        )

            











