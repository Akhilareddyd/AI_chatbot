import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace "*" with "http://localhost:5173" for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    prompt = f"""
    You are SolaceBot, a kind and empathetic AI friend supporting people through breakups and loneliness.
    Always respond with warmth and understanding. Here is the user's message:
    {request.message}
    """

    response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are SolaceBot, a compassionate friend."},
        {"role": "user", "content": request.message}
    ],
    temperature=0.7,
    max_tokens=250,)

    reply = response.choices[0].message.content

    return {"reply": reply}
