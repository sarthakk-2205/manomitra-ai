from transformers import pipeline
from threading import Lock

MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

# Model initially remains unloaded
classifier = None

# Prevent duplicate model loading
model_lock = Lock()


def get_sentiment_classifier():
    global classifier

    if classifier is None:
        with model_lock:
            if classifier is None:
                print("Loading sentiment analysis model...")

                classifier = pipeline(
                    "sentiment-analysis",
                    model=MODEL_NAME,
                    device=-1
                )

                print("Sentiment analysis model loaded!")

    return classifier


def analyze_sentiment(text: str) -> dict:

    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    sentiment_model = get_sentiment_classifier()

    result = sentiment_model(
        text[:2000],
        truncation=True
    )[0]

    return {
        "sentiment": result["label"].lower(),
        "confidence": round(float(result["score"]), 4),
        "model": MODEL_NAME
    }