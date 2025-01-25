# RAG-based Chatbot

## Overview
The **RAG-based Chatbot** is a PDF-powered search engine and chatbot built using **Retrieval-Augmented Generation (RAG)**. This application allows users to upload PDF documents, process their content, and interact with the document using natural language queries. The chatbot uses embeddings to extract context-relevant information and provides accurate and meaningful answers to user queries.

## Features
- **User Authentication**: Login and registration functionality to ensure secure and personalized access.
- **PDF Upload and Processing**: Allows users to upload PDFs, processes their content, and generates embeddings for search.
- **Contextual Question-Answering**: Users can query the uploaded PDFs, and the chatbot responds with answers derived from the document's content.
- **Chat History**: Maintains the history of user queries and chatbot responses for better interaction continuity.
- **User-Specific Indexing**: Each user's processed PDFs are stored and indexed separately for personalized search.

## Technologies Used
### Backend
- Python
- Streamlit (for UI)

### Database
- SQLite (for user and index management)

### Embedding Generation
- Custom embedding generation module

### PDF Processing
- `PdfLoader` for PDF parsing
- `Splitter` for document splitting

### LLM Query Execution
- Retrieval-Augmented Generation using `RunLLM`

## How It Works
### 1. User Login/Registration
- Users can create a new account or log in to an existing account.
- User credentials are securely validated through the SQLite database.

### 2. PDF Upload
- Users upload a PDF document.
- The PDF is processed:
  - Extracts text content.
  - Splits content into smaller chunks using the `Splitter`.
  - Creates embeddings using `CreateEmbeddings`.
- The processed data is saved with a unique index for the user.

### 3. PDF Search
- Once a PDF is processed, users can ask questions related to the document.
- Queries are passed to the `RunLLM` module, which retrieves the relevant context from the document's embeddings and generates a response using an LLM.

### 4. Interactive Chat
- Users can interact with the chatbot to ask multiple questions about the PDF.
- Both queries and answers are stored in session state to maintain chat history.

## Installation and Setup
### Prerequisites
- Python 3.8 or above
- Virtual environment setup (optional but recommended)

### Steps
1. **Clone the Repository**:
```bash
git clone <repository-url>
cd rag-based-chatbot
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the Application**:
```bash
streamlit run app.py
```

4. **Access the App**: Open your browser and navigate to `http://localhost:8501`.

## Directory Structure
```
├── app.py                  # Main application file
├── src/
│   ├── database.py         # Database management (SQLite)
│   ├── pdf_load.py         # PDF processing and text extraction
│   ├── split_docs.py       # Document splitting module
│   ├── create_embeddings.py# Embedding creation for documents
│   ├── query.py            # Query handling and RAG-based response generation
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Future Enhancements
- Add support for multi-format document uploads (e.g., Word, Excel)
- Incorporate advanced user analytics to track search and usage patterns
- Use cloud storage for PDF and embedding management for scalability
- Enhance the UI/UX for better interactivity
- Integrate more advanced LLMs and vector databases like Pinecone or Weaviate
