from RAG.vectorstore import get_retriever


def retrieve_documents(query: str, k: int = 4):
    """
    Retrieve relevant documents from the Chroma vector store.
    """

    retriever = get_retriever(k=k)

    documents = retriever.invoke(query)

    return documents


def format_documents(documents):
    """
    Convert retrieved documents into readable text.
    """

    formatted_documents = []

    for i, document in enumerate(documents, start=1):
        formatted_documents.append(
            f"--- Document {i} ---\n"
            f"{document.page_content}\n"
        )

    return "\n".join(formatted_documents)