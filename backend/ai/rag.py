import os

from dotenv import load_dotenv
from pinecone import Pinecone

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from ai.knowledge import KNOWLEDGE_BASE


load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY is missing")

if not PINECONE_INDEX_NAME:
    raise RuntimeError("PINECONE_INDEX_NAME is missing")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing")


# Pinecone client
pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index(
    PINECONE_INDEX_NAME
)


# Gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
    output_dimensionality=1536,
)


# LangChain Pinecone vector store
vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings,
)


def index_knowledge():
    documents = []

    for item in KNOWLEDGE_BASE:
        documents.append(
            Document(
                page_content=item["content"],
                metadata={
                    "title": item["title"]
                }
            )
        )

    ids = vector_store.add_documents(documents)

    return {
        "message": f"Indexed {len(ids)} documents",
        "ids": ids
    }


def search_knowledge(query: str):
    return vector_store.similarity_search(
        query,
        k=3
    )