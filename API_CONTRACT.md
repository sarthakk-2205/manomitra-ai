
# ManoMitra AI — API Contract

## Base URL
Local development: http://127.0.0.1:8000

## 1. Health Check

GET /health

Purpose: Check whether the AI service is running.

Expected response (example):
{
  "status": "ok"
}

## 2. General Chatbot

POST /chat

Request:
{
  "message": "How can I manage exam stress?"
}

Expected response:
{
  "reply": "A supportive response from the AI."
}

## 3. Sentiment Analysis

POST /sentiment

Request:
{
  "message": "I feel happy and motivated today."
}

Expected response (example):
{
  "sentiment": "positive",
  "confidence": 0.99,
  "model": "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
}

Note: The confidence is illustrative. Sentiment is not a
mental-health diagnosis or a crisis-risk assessment.

## 4. RAG Wellness Chat

POST /wellness-chat

Request:
{
  "message": "I feel overwhelmed by exams. What can I do?"
}

Normal response (example):
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

Possible-risk response (example):
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

## Request validation

- Send JSON with a non-empty "message" string.
- Current ChatRequest limits messages to 4000 characters.
- Empty or invalid requests may return HTTP 422.
- Sentiment validation errors may return HTTP 400.
- Server or upstream AI errors may return HTTP 500 or 502,
  depending on the endpoint.

## Important limitations

- Sentiment analysis predicts general English sentiment.
- RAG responses can still be inaccurate.
- Safety phrase screening can miss risk expressions.
- The service does not provide clinical diagnosis or
  emergency monitoring.
