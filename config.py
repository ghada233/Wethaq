import os
from dotenv import load_dotenv

load_dotenv()

MILVUS_URI = os.getenv("MILVUS_URI")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

IBM_WATSONX_API_KEY = os.getenv("IBM_WATSONX_API_KEY")
IBM_WATSONX_PROJECT_ID = os.getenv("IBM_WATSONX_PROJECT_ID")
IBM_WATSONX_URL = os.getenv("IBM_WATSONX_URL")
