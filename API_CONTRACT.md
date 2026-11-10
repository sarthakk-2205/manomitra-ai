# ManoMitra AI — API Contract

## 1. Base URL

Local development:

`http://127.0.0.1:8000`

Swagger documentation:

`http://127.0.0.1:8000/docs`

## 2. Health Check

**GET `/health`**

Purpose: Check whether the AI service is running.

Response:
```json
{
  "status": "healthy"
}
```

## 3. General Chatbot

**POST `/chat`**

Purpose: Generate a general AI chatbot response.

Request:
```json
{
  "message": "How can I manage exam stress?"
}
```

Response:
```json
{
  "reply": "A supportive response from the AI."
}
```

## 4. Sentiment Analysis

**POST `/sentiment`**

Purpose: Analyse general positive or negative sentiment.

Request:
```json
{
  "message": "I feel happy and motivated today."
}
```

Response:
```json
{
  "sentiment": "positive",
  "confidence": 0.99,
  "model": "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
}
```

Note: Confidence values are illustrative. Sentiment analysis is not a mental-health diagnosis or crisis-risk assessment.

## 5. Emotion Detection

**POST `/emotion`**

Purpose: Identify the predominant emotion expressed in a message.

Request:
```json
{
  "message": "I feel very lonely today."
}
```

Response:
```json
{
  "emotion": "sadness",
  "confidence": 0.98,
  "model": "j-hartmann/emotion-english-distilroberta-base"
}
```

Possible emotion labels include:
- Anger
- Disgust
- Fear
- Joy
- Neutral
- Sadness
- Surprise

Note: This is a general-purpose English emotion classifier, not a clinical assessment.

## 6. RAG Wellness Chat

**POST `/wellness-chat`**

Purpose: Generate wellness responses using information retrieved from the project's wellness documents. Includes basic safety phrase screening.

Request:
```json
{
  "message": "I feel overwhelmed by exams. What can I do?"
}
```

Normal response:
```json
{
  "reply": "A supportive answer grounded in retrieved resources.",
  "sources": [
    {
      "document": "who_doing_what_matters_in_times_of_stress.pdf",
      "page": 10
    }
  ],
  "safety": {
    "possible_risk": false,
    "resources": []
  }
}
```

Possible-risk response:
```json
{
  "reply": "Supportive safety guidance.",
  "sources": [],
  "safety": {
    "possible_risk": true,
    "resources": [
      {
        "name": "Tele-MANAS",
        "phone": "14416"
      },
      {
        "name": "Emergency services",
        "phone": "112"
      }
    ]
  }
}
```

## 7. Conversation Memory Chat

**POST `/memory-chat`**

Purpose: Generate responses using previous messages from the same session.

Request:
```json
{
  "session_id": "student_session_101",
  "message": "My exams are approaching and I feel stressed."
}
```

Response:
```json
{
  "session_id": "student_session_101",
  "reply": "A supportive response from the AI."
}
```

Use the same session ID for subsequent messages to maintain conversation context.

## 8. Memory + RAG Wellness Chat

**POST `/memory-rag-chat`**

Purpose: Combine conversation history with retrieved wellness information. Includes basic safety phrase screening.

Request:
```json
{
  "session_id": "student_session_101",
  "message": "Can you suggest some techniques for my situation?"
}
```

Normal response:
```json
{
  "session_id": "student_session_101",
  "reply": "A contextual wellness response.",
  "sources": [
    {
      "document": "who_doing_what_matters_in_times_of_stress.pdf",
      "page": 10
    }
  ],
  "safety": {
    "possible_risk": false,
    "resources": []
  }
}
```

Possible-risk response:
```json
{
  "session_id": "student_session_101",
  "reply": "Supportive safety guidance.",
  "sources": [],
  "safety": {
    "possible_risk": true,
    "resources": [
      {
        "name": "Tele-MANAS",
        "phone": "14416"
      },
      {
        "name": "Emergency services",
        "phone": "112"
      }
    ]
  }
}
```

## 9. Request Validation

For `ChatRequest`:
- `message` must be a string.
- Minimum length: 1 character.
- Maximum length: 4000 characters.

For `MemoryChatRequest`:
- `session_id` must be a string between 1 and 128 characters.
- `message` must be a string between 1 and 4000 characters.

Invalid request bodies may return HTTP 422.

Whitespace-only messages may return HTTP 400 or be rejected by endpoint validation.

## 10. Important Integration Notes

1. React should communicate with the Node.js backend.
2. Node.js should communicate with the FastAPI AI service.
3. Node.js should manage authentication and associate sessions with authenticated students.
4. MongoDB should store persistent chat history and other application data.
5. Never expose the Groq API key in frontend code.
6. The current Python conversation memory is stored in process memory and is not persistent across server restarts.
7. The AI service currently uses basic keyword-based safety screening. It can miss indirect, Hindi or Hinglish expressions of distress.
8. `/chat` and `/memory-chat` do not currently include safety screening. Do not use them as student-facing mental-wellness chat routes until safety handling is added.
9. The AI does not provide clinical diagnosis, prescribe medication or replace qualified counsellors.
10. Emotion and sentiment predictions should not be treated as clinical assessments or used for consequential student decisions.

## 11. Available Endpoints Summary

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Health check |
| POST | `/chat` | General chatbot |
| POST | `/sentiment` | Sentiment analysis |
| POST | `/emotion` | Emotion detection |
| POST | `/wellness-chat` | RAG wellness chatbot |
| POST | `/memory-chat` | Chatbot with memory |
| POST | `/memory-rag-chat` | Memory + RAG chatbot |