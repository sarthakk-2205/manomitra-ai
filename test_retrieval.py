
from app.rag import search_wellness_documents

questions = [
    "What are some practical ways to manage stress?",
    "How can young people improve their emotional well-being?",
    "What coping strategies can help during difficult times?"
]

for question in questions:
    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    results = search_wellness_documents(question, k=3)

    for i, doc in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Source:", doc.metadata.get("source", "Unknown"))
        print("Page:", doc.metadata.get("page", "Unknown"))
        print("Content:", doc.page_content[:700])
