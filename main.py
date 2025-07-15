from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel
from chatbot import get_chatbot_response, get_chat_history
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# Rate limiter configuration
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wesley-john.github.io"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/response schemas
class ChatRequest(BaseModel):
    user_id: str
    user_question: str

class ChatResponse(BaseModel):
    reply: str

class HistoryResponse(BaseModel):
    history: list  # list of [user, bot] pairs

# POST endpoint for chatbot interaction
@app.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
async def chat_endpoint(request: Request, chat: ChatRequest):
    user_id = chat.user_id.strip()
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required.")

    user_question = chat.user_question.strip()
    if not user_question:
        raise HTTPException(status_code=400, detail="Please provide a valid question.")

    reply = get_chatbot_response(user_question, user_id)
    return ChatResponse(reply=reply)

# GET endpoint for chat history retrieval
@app.get("/history", response_model=HistoryResponse)
@limiter.limit("10/minute")
async def history_endpoint(user_id: str = Query(..., description="User ID to retrieve history for")):
    history = get_chat_history(user_id)
    return HistoryResponse(history=history)

# Root health check
@app.get("/")
async def root():
    return {"message": "MeskottBot API is running"}