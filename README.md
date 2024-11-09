![WhatsApp Image 2024-11-09 at 12 19 33 PM](https://github.com/user-attachments/assets/7e725ad0-69b9-45dc-927a-a1d90114baea)

# Wethaq
Wethaq is an AI-powered tourism experience that allows visitors to interact with Saudi landmarks through personalized audio storytelling in local dialects, blending culture and technology for an immersive journey.

## Features

- **Flask-based Web Application**: A simple web server to handle API requests.
- **Semantic Search**: Uses Milvus and Sentence-Transformer to perform efficient similarity searches.
- **Text-to-Speech**: Converts Arabic text to speech using a multilingual TTS model.
- **Integration with IBM WatsonX**: Provides AI-powered text processing and data management.

```
Requirements
Flask: Python web framework for building the application.
Sentence-Transformer: Used for generating text embeddings.
Milvus: A vector database for efficient similarity search.
IBM WatsonX API: Optional, for leveraging AI services (like NLP, AI models).
Install the required Python libraries:

```bash
pip install -r requirements.txt
```
Note: Ensure that Milvus is running locally or on a remote server and that IBM WatsonX credentials are properly set in the .env file.

---

## Installation

Clone the repository:

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


## Docker and Docker Compose Setup

To run the **Wethaq** Flask application in a containerized environment using Docker and Docker Compose, follow these steps:

### 1. **Docker Setup**

Make sure Docker and Docker Compose are installed on your system. If not, follow the official installation guides:

- **Docker**: [Get Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Get Docker Compose](https://docs.docker.com/compose/install/)

### 2. **Build Docker Image**

In the project root directory, where the `Dockerfile` is located, run the following command to build the Docker image:

```bash
docker build -t wethaq-app .
```

This will build the image for the Wethaq application.

### 3. **How to deploy it locally **

To run this project on your machine, you have to clone it and simply run a

```bash
docker compose up -d
```

---
License

```bash
🪪 Allam License: https://github.com/metallama/llama/blob/main/LICENSE
```
```bash
🪪 License: This project is licensed under the MIT License - see the LICENSE file for details. 
```
