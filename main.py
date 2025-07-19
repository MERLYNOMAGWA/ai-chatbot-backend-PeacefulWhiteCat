from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import get_chatbot_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wesley-john.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_question: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_question = request.user_question.strip()
    if not user_question:
        raise HTTPException(status_code=400, detail="Please provide a valid question.")

    reply = get_chatbot_response(user_question)
    return ChatResponse(reply=reply)

@app.get("/")
async def root():
    return {"message": "MeskottBot API is running"}