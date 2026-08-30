import os

from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client, Client

# Load variables from .env
load_dotenv()

app = FastAPI(
    title="AI User Management API",
    version="1.0.0"
)

# Read Supabase environment variables
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")

# Check that variables exist
if not SUPABASE_URL:
    raise RuntimeError("NEXT_PUBLIC_SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise RuntimeError(
        "NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY is missing from .env"
    )

# Create Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


@app.get("/")
def root():
    return {
        "message": "AI User Management API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/test-supabase")
def test_supabase():
    try:
        response = (
            supabase
            .table("users")
            .select("*")
            .limit(1)
            .execute()
        )

        return {
            "status": "success",
            "message": "Supabase connection is working",
            "data": response.data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
from routes.users import router as users_router

app.include_router(users_router)

from routes.chat import router as chat_router

app.include_router(chat_router)