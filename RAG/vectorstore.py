from langchain_chroma import Chroma
from RAG.embeddings import get_embedding_model
vectorstore_dir = "chroma_db"

collection_name = "research_documents"

def create_vectorstore(chunks):
    """
    Create a Chroma vector store from document chunks.
    """
    embedding = get_embedding_model()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=vectorstore_dir,
        collection_name=collection_name
    )
    return vectorstore

def load_vectorstore():
    """
    Load an existing Chroma vector store.
    """

    embedding = get_embedding_model()

    vectorstore = Chroma(
        persist_directory=vectorstore_dir,
        embedding_function=embedding,
        collection_name=collection_name
    )
    return vectorstore


def get_retriever(k=4):
    """
    Create a retriever from the vector store.
    """

    vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        }
    )

    return retriever