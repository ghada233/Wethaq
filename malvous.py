import os
from dotenv import load_dotenv
from src.ALLAM import IBMWatsonXAIWrapper
from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility
from sentence_transformers import SentenceTransformer
import glob

# Load environment variables
load_dotenv()

# Initialize IBM WatsonX AI Wrapper
api_key = os.getenv("IBM_WATSONX_API_KEY") or 't7YJ-yWRGikWjOtoJ6TSBpWcDvUBldkDHHbyMtOyhq7Q'
project_id = os.getenv("IBM_WATSONX_PROJECT_ID") or 'a29156ce-b814-46b8-aa88-a21e0243a084'
url = os.getenv("IBM_WATSONX_URL", "https://eu-de.ml.cloud.ibm.com")
# wrapper = IBMWatsonXAIWrapper(api_key, project_id, url)

# # Initialize Milvus connection
connections.connect("default", host="127.0.0.1", port="19530")

def create_embedding():
    # Initialize the SentenceTransformer for embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Example model, change as needed

    # Load text files and generate embeddings
    texts = []
    embeddings = []
    for filepath in glob.glob("/Users/kamel402/Desktop/Hackathons/ALLAM/Wethaq/data/*.txt"):  # Update the path accordingly
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            texts.append(text)
            embedding = model.encode(text).tolist()  # Convert embedding to list for Milvus
            embeddings.append(embedding)


    dim = 384  # Replace with your actual dimension

    adjusted_embeddings = [emb + [0] * (dim - len(emb)) for emb in embeddings]  # Pad to correct dim

    embedding_sample = adjusted_embeddings[0]  # Get the first embedding as a sample
    dim = len(embedding_sample)
    print("Embedding dimension:", dim)
    return texts, adjusted_embeddings, model

def create_collection(collection_name, dim, text_max_length):
    # Define collection name

    # Define fields for the schema
    id_field = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True)
    embedding_field = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)  # Adjust 'dim' to the actual dimension of your embeddings
    text_field = FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=text_max_length)  # VARCHAR field for text, adjust max_length if necessary

    # Create schema
    schema = CollectionSchema(fields=[id_field, embedding_field, text_field], description="Collection of Saudi landmarks embeddings", enable_dynamic_field=True)

    # Create the collection with the schema
    collection = Collection(name=collection_name, schema=schema)

    print(f"Collection '{collection_name}' created successfully!")
    return collection

def delete_collection(collection):
    collection.drop()

    print(f"Collection '{collection}' has been deleted.")

def clear_data(collection):
    # Insert embeddings and text into Milvus
    if not collection.is_empty:
        collection.delete("")  # Optional: Clear existing data

# Assuming `texts` are available for your data, or you can generate colors from `texts` (or some other logic)
def transform_entities_to_data(texts, embeddings):
    data = []
    data = []
    for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        # Create the new structure
        data_entry = {
            "text": text,  # Sequential ID
            "embedding": embedding,  # Embedding vector
        }
        data.append(data_entry)
    return data


def prepare_data(texts, embeddings, collection):
    # Create IDs for the texts
    # ids = [i for i in range(len(texts))]

    # Prepare data for Milvus in the correct format
    entities = [
        # {"name": "id", "values": ids, "type": "INT64"},  # ID field for primary key
        {"name": "text", "values": texts, "type": "VARCHAR"},  # Text field for reference
        {"name": "embedding", "values": embeddings, "type": "FLOAT_VECTOR"}  # Embedding field
    ]
    data = transform_entities_to_data(texts, embeddings)
    # Insert data into the Milvus collection
    collection.insert(data)
    print("Data inserted successfully!")

# Function to retrieve relevant context based on query
def retrieve_relevant_context(collection_name, model, collection, query_text, top_k=3):
    query_embedding = model.encode(query_text).tolist()
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        # output_fields=["text"]
    )
    return " ".join([result.entity.get("text") for result in results[0]])


texts, adjusted_embeddings, model = create_embedding()
# adjusted_embeddings = [
#     [0.1] * 4,  # First embedding (replace with real data)
#     [0.2] * 4   # Second embedding (replace with real data)
# ]
# texts = ['sdcscs', 'erererre']
# collection = create_collection('saudi_landmarks', 4, 10000)
collection_name = 'saudi_landmarks'
collection = create_collection(collection_name, 384, 10000)
# delete_collection(collection)
# clear_data(collection)
prepare_data(texts, adjusted_embeddings, collection)
# # Example prompt
user_query = f"اكتبلي تاريخ Kingdom Tower بشكل مختصر"


context = retrieve_relevant_context(collection_name, model, collection, user_query)

# # # Generate text with the context-enhanced prompt
# prompt = f"Context: {context}\n\nPrompt: {user_query}"
# # generated_text = wrapper.generate_text(prompt)
print(context)
# print(prompt)
