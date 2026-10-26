
from transformers import pipeline

MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

# Load the pretrained sentiment model once
classifier = pipeline(
    "sentiment-analysis",
    model=MODEL_NAME,
    device=-1
)


def analyze_sentiment(text: str) -> dict:
    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    result = classifier(text[:2000], truncation=True)[0]

    return {
        "sentiment": result["label"].lower(),
        "confidence": round(float(result["score"]), 4),
        "model": MODEL_NAME
    }
