from transformers import pipeline
from threading import Lock

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

# Model will initially remain unloaded
emotion_classifier = None

# Prevent multiple model loads during simultaneous requests
model_lock = Lock()


def get_emotion_classifier():
    global emotion_classifier

    if emotion_classifier is None:
        with model_lock:
            if emotion_classifier is None:
                print("Loading emotion detection model...")

                emotion_classifier = pipeline(
                    "text-classification",
                    model=MODEL_NAME,
                    device=-1
                )

                print("Emotion detection model loaded!")

    return emotion_classifier


def analyze_emotion(text: str) -> dict:

    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    classifier = get_emotion_classifier()

    result = classifier(
        text[:2000],
        truncation=True
    )[0]

    return {
        "emotion": result["label"].lower(),
        "confidence": round(float(result["score"]), 4),
        "model": MODEL_NAME
    }