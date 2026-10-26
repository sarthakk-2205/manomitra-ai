
from app.rag import build_vector_store

if __name__ == "__main__":
    print("Building ManoMitra wellness knowledge base...")

    vector_store, chunk_count = build_vector_store()

    print(f"Knowledge base created successfully!")
    print(f"Total text chunks: {chunk_count}")
    print("Stored in: chroma_db/")
