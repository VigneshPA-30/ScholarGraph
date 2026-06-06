from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma




class DocumentLoader:
    def __init__(self):
        pass

    def PdfLoader(self, pdfpath):
        loader = PyPDFLoader(pdfpath)
        docs = loader.load()
        return docs





class Embeddings:
    def __init__(self):
        self.docLoader = DocumentLoader()

    def PdfEmbeddings(self, model, pdfpath):

        docs = self.docLoader.PdfLoader(pdfpath)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)

        embeddings = model.TextembeddingModelInvoke()

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./db"
        )

        # vector_db.persist()

        retriever = vector_db.as_retriever(
            search_kwargs={"k":5}        
        )

        return retriever







