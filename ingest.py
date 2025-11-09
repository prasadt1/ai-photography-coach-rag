# ingest.py
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Define the path to your data and the path to save the index
DATA_PATH = "data"
DB_PATH = "faiss_index"

def create_vector_db():
    """
    Reads all PDF documents from the DATA_PATH,
    splits them into chunks, creates embeddings,
    and saves them to a local FAISS vector store.
    """
    documents = []  # FIX: Initialize empty list
    
    # Loop through all files in the 'data' folder
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DATA_PATH, filename)
            print(f"Loading {filename}...")
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())
    
    if not documents:
        print("No PDF documents found in the 'data' folder.")
        return

    print(f"Loaded {len(documents)} pages from PDF documents.")

    # Split the documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")
    
    # Define the embedding model. This runs locally.
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create the FAISS vector store from the chunks
    print("Creating vector store (this may take 2-3 minutes)...")
    db = FAISS.from_documents(chunks, embeddings)
    
    # Save the vector store locally
    db.save_local(DB_PATH)
    print(f"✅ Vector store created and saved to {DB_PATH}")

if __name__ == "__main__":
    create_vector_db()
