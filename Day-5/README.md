#  Campus Buddy – Day 5 (RAG)

## 1. What the Task Is & System Chosen

**Task:** Implement a Retrieval-Augmented Generation (RAG) system using a college PDF.

**System Chosen:** Campus Buddy – AI-powered College Helpdesk Assistant.

The system retrieves relevant information from a college handbook PDF and generates answers using Groq LLM.

**Technologies Used:**
- Python
- Google Colab
- PyPDF
- Sentence Transformers
- FAISS
- Groq API
- NumPy
- LangChain Text Splitters

## 2. Core Implementation & Outputs

- **Cell 1:** Installed required libraries.
- **Cell 2:** Uploaded PDF and extracted text.
- **Cell 3:** Split text into chunks using `RecursiveCharacterTextSplitter`.
- **Cell 4:** Generated embeddings using `all-MiniLM-L6-v2`.
- **Cell 5:** Created FAISS vector index.
- **Cell 6:** Configured Groq API.
- **Cell 7:** Retrieved relevant context using FAISS similarity search.
- **Cell 8:** Generated answers using Groq LLM.
- **Cell 9:** Tested Campus Buddy with college-related questions.
- **Cell 10:** Created an interactive question-answering system.

## 3. "Your 30%" – Hands-On Work & Observations

- Used a sample college handbook PDF as the knowledge source.
- Experimented with text chunking and overlap.
- Generated embeddings and stored them in FAISS.
- Implemented context retrieval using similarity search.
- Integrated Groq LLM for answer generation.
- Tested different college-related questions.
- Observed how RAG generates answers using retrieved document context.

## 4. How to Run

**Google Colab:**  
https://colab.research.google.com/drive/1fhbxNw-Hi-cTJKnOUtzfKGm_EvS_oi4w?usp=sharing

1. Open the Colab notebook.
2. Run the cells sequentially.
3. Upload the sample college PDF.
4. Enter the Groq API key.
5. Test questions using Campus Buddy.

**Day 5 Outcome:** Successfully implemented a basic PDF-based RAG system using Sentence Transformers, FAISS and Groq LLM.
