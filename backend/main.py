import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client


# Load variables from .env
load_dotenv()


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="AI User Management API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# SUPABASE CONFIGURATION
# =========================================================

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")


if not SUPABASE_URL:
    raise RuntimeError(
        "NEXT_PUBLIC_SUPABASE_URL is missing from .env"
    )


if not SUPABASE_KEY:
    raise RuntimeError(
        "NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY is missing from .env"
    )


# =========================================================
# SUPABASE CLIENT
# =========================================================

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# BASIC ROUTES
# =========================================================

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


# =========================================================
# SUPABASE TEST
# =========================================================

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


# =========================================================
# USER ROUTES
# =========================================================

from routes.users import router as users_router

app.include_router(users_router)


# =========================================================
# CHAT ROUTES
# =========================================================

from routes.chat import router as chat_router

app.include_router(chat_router)