from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

def split_documents(documents):
    """
    Split documents into smaller chunks for RAG retrievel.

    Args: 
        documents: List of langchin Documents objects.

    Returns : 
        List of chumked Document objects.     
    """

    text_splitter = RecursiveCharacterTextSplitter(
        Chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Original documents : {len(documents)}")
    print(f"Generated chunks : {len(chunks)}")
    return chunks