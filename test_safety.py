
from app.safety import check_safety

tests = [
    "I am stressed about exams.",
    "I want to die.",
]

for message in tests:
    print("\nInput:", message)
    print(check_safety(message))
