from fastapi import APIRouter
from pydantic import BaseModel

from ai.agent import run_agent


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(request: ChatRequest):

    response = await run_agent(
        request.message
    )

    return {
        "message": response
    }