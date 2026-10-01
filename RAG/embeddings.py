from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = "sentence-transformers/all-MiniLM-L6-v2"

def get_embedding_model():
    """
    Create and return the Hugging Face embedding model.
    """
    embedings = HuggingFaceEmbeddings(
        model_name = embedding_model, 
        model_kwargs={
            "device":"cpu"
        },
        encode_kwargs={
            "normalize_embeddings" : True
        }
    )

    return embedings