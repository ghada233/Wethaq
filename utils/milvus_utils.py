import os
from sentence_transformers import SentenceTransformer
from pymilvus import MilvusClient
from config import MILVUS_URI, COLLECTION_NAME

# Initialize the Milvus client globally (loaded once)
milvus_client = MilvusClient(uri=MILVUS_URI)
collection_name = COLLECTION_NAME

# Initialize the Sentence-Transformer model globally (loaded once)
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')


def emb_text(text):
    """
    Generate embeddings for a single text input using SentenceTransformer.
    
    Args:
    text (str): The input text for which embeddings are to be generated.

    Returns:
    list: The generated embedding as a list.
    """
    embedding = model.encode(text).tolist()  # Convert embedding to list for Milvus
    return embedding


def get_context(query_text, limit=3):
    """
    Retrieve the context (most similar documents) for the given query text 
    from Milvus by performing a similarity search.

    Args:
    query_text (str): The input query text to search in Milvus.
    limit (int): Number of top similar results to return.

    Returns:
    list: A list of dictionaries containing the most similar text documents and their distances.
    """
    query_embedding = emb_text(query_text)  # Get the embedding for the query

    # Perform the search in Milvus
    search_res = milvus_client.search(
        collection_name=collection_name,
        data=[query_embedding],  # Search for the embedding
        limit=limit,  # Retrieve top N most similar results
        search_params={"metric_type": "L2", "params": {"nprobe": 10}},  # Euclidean distance metric
        output_fields=["text"]  # Retrieve the 'text' field from the search results
    )
    
    # Process and return the results
    context = []
    for result in search_res:
        for res in result:
            context.append({
                "text": res.entity.get("text", ""),
                "distance": res.distance  # The distance measure from the query
            })

    return context

