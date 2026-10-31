from app.emotion import analyze_emotion

messages = [
    "I am feeling very lonely today.",
    "I am so happy about my achievements!",
    "I am scared about my future.",
    "I am extremely angry right now.",
    "Everything is normal today."
]

for message in messages:
    print("\nMessage:", message)
    print("Result:", analyze_emotion(message))