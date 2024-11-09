# Wethaq

Wethaq is a smart product that aims to provide an unprecedented tourism experience in the Kingdom. Using artificial intelligence technologies and large language models (LLMs), the product allows visitors to interact with Saudi landmarks in personal and innovative ways. Simply, visitors can point their cameras towards any tourist landmark to be greeted with audio content and storytelling in a local dialect that reflects the culture of the region.
Wathaq, exploring Saudi culture
Description of the idea
Whether you are touring the Masmak Palace in Riyadh, or enjoying the southern heritage in Asir, Wathaq will make the experience interactive and personal, blending the past and the present, and allowing visitors to immerse themselves in the details of the place.

## Features

- **Flask-based Web Application**: A simple web server to handle API requests.
- **Semantic Search**: Uses Milvus and Sentence-Transformer to perform efficient similarity searches.
- **Text-to-Speech**: Converts Arabic text to speech using a multilingual TTS model.
- **Integration with IBM WatsonX**: Provides AI-powered text processing and data management.


## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Wethaq.git
cd Wethaq
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Ensure that you have Milvus, IBM WatsonX, and other necessary services set up.
Configuration
Set Up Environment Variables
Create a .env file in the root directory of the project and add the following configuration settings:
```

## Milvus Setup
This project uses Milvus for fast vector similarity search. Here's a basic guide on how to integrate Milvus with the application:

Install Milvus: You need to have Milvus installed and running. You can follow the Milvus installation guide here: Milvus Installation.

Connecting to Milvus: The Milvus client will connect to your local or remote Milvus instance through the MILVUS_URI. The collection name to store the data in is specified by the COLLECTION_NAME.

Sentence-Transformer and Milvus Integration
Embedding Text: The SentenceTransformer model is used to generate embeddings for the text that you want to search. This embedding is then used for similarity search in Milvus.

## Running the Application
To run the Flask application, execute the following command:

bash
Copy code
flask run
This will start the server, and you can interact with the API at http://127.0.0.1:5000.

API Endpoints
Generate Speech
Converts input text into speech and saves it as a file.

Endpoint: /generate_speech

Method: POST

Request Body:

json
Copy code
{
  "text": "Your text here",
  "language": "ar"  # Optional, default is Arabic (ar)
}
Response:

json
Copy code
{
  "message": "Speech generated successfully",
  "audio_file": "/path/to/generated_audio.wav"
}
Search in Milvus
Performs a semantic search in Milvus for the most similar text.

Endpoint: /search

Method: POST

Request Body:

json
Copy code
{
  "query": "Your query text here"
}
Response:

json
Copy code
{
  "results": [
    {
      "text": "Most similar document text",
      "distance": 0.1234
    }
  ]
}
Requirements
Flask: Python web framework for building the application.
Sentence-Transformer: Used for generating text embeddings.
Milvus: A vector database for efficient similarity search.
IBM WatsonX API: Optional, for leveraging AI services (like NLP, AI models).
Install the required Python libraries:

bash
Copy code
pip install -r requirements.txt
Note: Ensure that Milvus is running locally or on a remote server and that IBM WatsonX credentials are properly set in the .env file.

License
This project is licensed under the MIT License - see the LICENSE file for details.

yaml
Copy code

---

### Key Sections:

- **Setup Instructions**: How to set up the environment, install dependencies, and configure the environment variables.
- **Milvus Integration Guide**: Provides the code for embedding text and performing semantic search with Milvus.
- **Running the Application**: Explains how to start the Flask app and interact with the API.
