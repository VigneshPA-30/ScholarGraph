from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker

from langchain_chroma import Chroma
import hashlib, json
from unstructured.partition.auto import partition
from typing import List, Dict
from pathlib import Path
from pydantic import BaseModel, Field
import time
from tenacity import retry, stop_after_attempt, wait_exponential


class ChunkingOutput(BaseModel):
    detailed_text:str=Field(description="Detailed description of the given input by the LLM")




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


class DocumentProcessor:
    def __init__(self, model):
        self.docLoader = DocumentLoader()
        self.embeddings_model = model.textembeddingModelInvoke()
        self.chunkingModelInvoke = model.chunkingModelInvoke()
        # self.textSplitter = SemanticChunker(embeddings = self.embeddings_model)
        self.textSplitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
        self.vector_db = Chroma(persist_directory="./db", embedding_function=self.embeddings_model,)


    def startprocessing(self, doc_paths:List):
        for doc_path in doc_paths:
            if not self.docLoader.isProcessed(doc_path):
                if not self.chunkingDocs(str(doc_path)):
                    return False
        return True

    def chunkingDocs(self,doc_path:str):
        hash_value = self.docLoader.getHash(doc_path)
        # elements = partition(filename=doc_path,
        #                      strategy="hi_res",
        #                      extract_image_block_output_dir="utils/imageoutputs/",
        #                      extract_images_in_pdf=True)
        elements = partition(filename=doc_path, strategy="fast")
        chunks = []
        current_title = ""
        texts_to_embed = []
        metadatas_to_embed = []
        try:
            for element in elements:
                element_type = element.category
                page_no = getattr(element.metadata, "page_number", None)  
                

                if element.category in ["Title", "Header"]:
                    current_title = element.text
                elif element_type in ["NarrativeText", "ListItem"]:
                    # print(element.text)
                    # chunk = self.embedText(f"Title:{current_title}\n\n {element.text}", page_no, doc_path, hash_value)
                    # chunks.extend(chunk)
                    texts_to_embed.append(f"Title:{current_title}\n\n {element.text}")
                    metadata = {
                                "page_no":page_no,
                                "doc_path":doc_path,
                                "pdf_hash":hash_value
                            }
                    metadatas_to_embed.append(metadata)

                elif element_type == "Table":
                    pass

                elif element_type == "Image":
                    # You could instead send the extracted image to a vision model
                    pass

            chunks = self.embedTextBtach(texts_to_embed, metadatas_to_embed)
            self.savetoVectorDB(chunks)
            self.docLoader.storeHash(hash_value,doc_path)
            return True 
        except Exception as e:
            print(f"Error processing {doc_path}: {e}")
            return False
                
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=60))
    def embedTextBtach(self, texts:List[str],metadatas:List[Dict]):
   

        # print(text)
        chunks = self.textSplitter.create_documents(texts = texts,
                                               metadatas = metadatas)
        
        return chunks

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=12, max=65))
    def _add_batch_with_retry(self, batch):
        self.vector_db.add_documents(batch)

    def savetoVectorDB(self, chunks):
        # We cap the batch size at 80 to comfortably stay under the 100/min limit.
        batch_size = 80 
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            print(f"Embedding batch {i//batch_size + 1} ({len(batch)} chunks)...")
            
            # This handles transient network failures
            self._add_batch_with_retry(batch)
            
            # If there are more chunks left, we MUST wait 60 seconds to reset the free tier quota
            if i + batch_size < len(chunks):
                print("Batch successful. Sleeping for 60 seconds to respect API rate limits...")
                time.sleep(60)

    # def PdfEmbeddings(self, pdfpath):
    #     print(f"pdf_path inside Embeddings {pdfpath}")
    #     hash_value = self.docLoader.getHash(pdfpath)

    #     if not self.docLoader.isProcessed(pdfpath):

    #         docs = self.docLoader.PdfLoader(pdfpath)
    #         for doc in docs:
    #             doc.metadata["pdf_hash"] = hash_value
    #             # print("DOC",doc)

    #         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    #         chunks = text_splitter.split_documents(docs)  

    #         # print("LENCHUNKS",len(chunks))      

    #         vector_db = Chroma.from_documents(
    #             documents=chunks,
    #             embedding=self.embeddings_model,
    #             persist_directory=f"./db"
    #         )
    #         self.docLoader.storeHash(hash_value,pdfpath)
        
           

    #     return hash_value

    def getRetriever(self):
        search_kwargs = {"k":5}
        # print(selectedHashes)
        # if selectedHashes:
        #     search_kwargs["filter"]={
        #         "pdf_hash":{
        #         "$in":selectedHashes
        #         }
        #     }

        vector_db = Chroma(
                persist_directory=f"./db",
                embedding_function=self.embeddings_model
            )
        

        return vector_db.as_retriever(
                search_kwargs= search_kwargs
        )

            











