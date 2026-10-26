
from functools import lru_cache
from pathlib import Path
import shutil

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = ROOT / "documents"
CHROMA_DIR = ROOT / "chroma_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "manomitra_wellness"


@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vector_store():
    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {DOCUMENTS_DIR}"
        )

    documents = []

    for pdf_path in pdf_files:
        pages = PyPDFLoader(str(pdf_path)).load()

        for page in pages:
            text = " ".join(page.page_content.split())

            # Skip covers and nearly empty pages
            if len(text) < 120:
                continue

            page.page_content = text
            page.metadata["source"] = pdf_path.name
            documents.append(page)

    if not documents:
        raise ValueError(
            "No usable text found. Check whether the PDFs "
            "contain selectable text or need OCR."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No text chunks were created.")

    # Rebuilding starts with a clean local database.
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    store = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )

    # Clear any previously cached store after rebuilding.
    get_vector_store.cache_clear()

    return store, len(chunks)


@lru_cache(maxsize=1)
def get_vector_store():
    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            "Knowledge base not found. Run build_knowledge_base.py first."
        )

    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embeddings(),
        collection_name=COLLECTION_NAME,
    )


def search_wellness_documents(question: str, k: int = 3):
    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    results = get_vector_store().similarity_search_with_relevance_scores(
        question,
        k=k,
    )

    # Initial threshold; tune using representative test questions.
    return [
        doc
        for doc, score in results
        if score >= 0.25
    ]
