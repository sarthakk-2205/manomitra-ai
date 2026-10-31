# ManoMitra AI

### AI-Powered Mental Wellness Assistant for College Students

ManoMitra AI is the artificial intelligence component of ManoMitra, a digital mental wellness and psychological support platform designed for students in higher education.

It provides empathetic conversational support, document-grounded wellness information, emotion detection, sentiment analysis and basic safety screening.

The AI service is developed using Python and FastAPI, with Groq-powered language models, Retrieval-Augmented Generation (RAG), ChromaDB and Hugging Face Transformers.

---

## 1. Features

### AI Conversational Chatbot
- Powered by Groq LLMs.
- Provides empathetic and supportive conversational responses.
- Designed for general student wellness discussions.
- Uses customized system instructions.

### Retrieval-Augmented Generation (RAG)
- Retrieves relevant information from wellness documents.
- Uses LangChain document loaders and text splitters.
- Stores document embeddings in ChromaDB.
- Uses Hugging Face sentence-transformer embeddings.
- Returns source document names and page references.
- Reduces dependence on unsupported general model knowledge.

### Sentiment Analysis
- Uses a pretrained DistilBERT sentiment classification model.
- Classifies text into positive and negative sentiment.
- Returns prediction confidence.

### Emotion Detection
- Uses `j-hartmann/emotion-english-distilroberta-base`.
- Identifies seven emotion categories:
  - Anger
  - Disgust
  - Fear
  - Joy
  - Neutral
  - Sadness
  - Surprise

### Basic Safety Screening
- Uses predefined keyword and phrase matching.
- Identifies certain expressions associated with distress and possible self-harm.
- Provides supportive guidance and configured Indian emergency resources.

This is a basic prototype mechanism, not a clinically validated crisis-detection system.

### Conversation Memory
- Maintains conversation history using session IDs.
- Supports contextual follow-up questions.
- Retains the latest 20 messages per session.
- Supports memory-enabled RAG responses.

**Note:** Current conversation memory is stored in application memory and is not persistent across server restarts.

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core AI development |
| FastAPI | REST API development |
| Groq | LLM inference |
| LangChain | Document processing and RAG |
| ChromaDB | Vector database |
| Hugging Face Transformers | Sentiment and emotion analysis |
| Sentence Transformers | Text embeddings |
| PyPDF | PDF document loading |
| Pydantic | API request validation |
| Uvicorn | ASGI server |

---

## 3. Project Structure

```text
MANOMITRA AI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── chatbot.py
│   ├── rag.py
│   ├── safety.py
│   ├── sentiment.py
│   ├── emotion.py
│   └── memory.py
│
├── documents/
│   ├── UNICEF_Workbook_FINAL.pdf.pdf
│   └── who_doing_what_matters_in_times_of_stress.pdf
│
├── build_knowledge_base.py
├── test_retrieval.py
├── test_safety.py
├── test_sentiment.py
├── test_emotion.py
│
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

---

## 4. Installation and Setup

### Prerequisites

- Python 3.11 or later (Python 3.12 recommended).
- Git.
- Groq API key.

### Step 1: Clone the repository

```bash
git clone https://github.com/sarthakk-2205/manomitra-ai.git
```

Navigate into the project:

```bash
cd manomitra-ai
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_supported_groq_model
```

Replace the placeholder values with your actual credentials and supported model identifier.

Never commit `.env` or expose API keys in frontend code.

### Step 5: Build the knowledge base

```bash
python build_knowledge_base.py
```

This processes the wellness PDFs and creates the local ChromaDB knowledge base.

Run this command after cloning the repository or whenever the source documents change.

### Step 6: Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 5. API Endpoints

Base URL:

```text
http://127.0.0.1:8000
```

### GET /health

Checks whether the AI service is running.

### POST /chat

Generates a general AI chatbot response.

Request:

```json
{
  "message": "I am feeling stressed about my exams."
}
```

### POST /sentiment

Analyzes the sentiment of the supplied text.

Request:

```json
{
  "message": "I am feeling happy today."
}
```

Response fields:

```json
{
  "sentiment": "positive",
  "confidence": 0.99,
  "model": "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
}
```

Actual confidence values depend on the model output.

### POST /emotion

Predicts the emotion expressed in the supplied text.

Request:

```json
{
  "message": "I am feeling very lonely today."
}
```

Response fields:

```json
{
  "emotion": "sadness",
  "confidence": 0.98,
  "model": "j-hartmann/emotion-english-distilroberta-base"
}
```

### POST /wellness-chat

Provides a basic safety-screened, RAG-based wellness response.

Request:

```json
{
  "message": "How can I manage exam stress?"
}
```

Response structure:

```json
{
  "reply": "AI-generated response",
  "sources": [],
  "safety": {
    "possible_risk": false,
    "resources": []
  }
}
```

### POST /memory-chat

Generates a response using session-based conversation history.

Request:

```json
{
  "session_id": "student_001",
  "message": "What is my name?"
}
```

Response structure:

```json
{
  "session_id": "student_001",
  "reply": "AI-generated response"
}
```

### POST /memory-rag-chat

Combines conversation memory with document retrieval.

Request:

```json
{
  "session_id": "student_001",
  "message": "How can I manage exam stress?"
}
```

Response structure:

```json
{
  "session_id": "student_001",
  "reply": "AI-generated response",
  "sources": [
    {
      "document": "wellness_document.pdf",
      "page": 10
    }
  ]
}
```

**Integration note:** `/memory-rag-chat` currently does not perform safety screening. `/wellness-chat` performs basic safety screening but does not use conversation memory. Do not expose the memory-RAG endpoint as the final student-facing wellness endpoint until safety screening has been integrated into that flow.

All POST endpoints use JSON request bodies. Refer to `/docs` for the exact current response schemas and error responses.

---

## 6. Integration Architecture

ManoMitra uses a service-based architecture.

```text
React Frontend
      |
      v
Node.js / Express Backend
      |
      v
Python FastAPI AI Service
      |
      +---- Groq LLM
      |
      +---- ChromaDB RAG
      |
      +---- Hugging Face Models
      |
      +---- Safety Screening
      |
      +---- Conversation Memory
```

The frontend should communicate with the Node.js backend.

The Node.js backend should forward appropriate AI requests to the Python FastAPI service.

The Groq API key must remain on the server side.

For production, use authenticated user-to-session mapping and persistent conversation storage rather than trusting arbitrary session IDs or relying on Python process memory.

---

## 7. Testing

Run the individual test scripts from the project root:

```bash
python test_retrieval.py
```

```bash
python test_safety.py
```

```bash
python test_sentiment.py
```

```bash
python test_emotion.py
```

The API can also be tested through FastAPI Swagger documentation at `/docs`.

---

## 8. Important Limitations

ManoMitra AI is an academic prototype intended for general student wellness support.

- It does not diagnose mental-health conditions.
- It does not prescribe medication.
- Emotion and sentiment predictions are not clinical assessments.
- Emotion classification is English-focused.
- Safety screening uses basic keyword matching and may miss indirect or multilingual expressions of distress.
- The chatbot is not a replacement for a qualified mental-health professional.
- Conversation memory is currently in-memory and temporary.
- RAG responses depend on the quality and relevance of the indexed documents.
- Source references indicate retrieved passages; they do not independently establish that every generated claim is supported.

Students experiencing serious distress should be encouraged to seek qualified human support. Emergency resources must be verified before deployment.

---

## 9. Future Scope

Potential future improvements include:

- Persistent conversation storage.
- Improved multilingual safety screening.
- Better retrieval relevance and evaluation.
- Authentication-linked session management.
- Cloud deployment.
- More comprehensive API and integration testing.

---

## 10. Contributors

**Project:** ManoMitra — Digital Mental Health and Psychological Support System for Students in Higher Education.

**AI Module:** Python, FastAPI, Groq, RAG, ChromaDB and Hugging Face.

**AI Repository:**  
https://github.com/sarthakk-2205/manomitra-ai

---

## Disclaimer

ManoMitra AI is an educational project and is not a medical device or emergency-response service. Its responses may be inaccurate or incomplete. Users should seek qualified professional support for mental-health concerns.
