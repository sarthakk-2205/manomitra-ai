from transformers import pipeline

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

# Load the emotion model once
emotion_classifier = pipeline(
    "text-classification",
    model=MODEL_NAME,
    device=-1
)


def analyze_emotion(text: str) -> dict:

    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    result = emotion_classifier(
        text[:2000],
        truncation=True
    )[0]

    return {
        "emotion": result["label"].lower(),
        "confidence": round(float(result["score"]), 4),
        "model": MODEL_NAME
    }