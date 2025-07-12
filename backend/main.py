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



from typing import List, Dict

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]]  # [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]


@app.post("/chat")
async def chat(request: ChatRequest):

    system_prompt = """You are a compassionate and empathetic AI companion specialized in providing emotional support for people going through breakups and relationship challenges. Your role is to:

                    1. Listen actively and validate emotions without judgment
                    2. Provide gentle, practical coping strategies and advice
                    3. Offer perspective while being sensitive to the person's current emotional state
                    4. Encourage healthy healing processes and self-care
                    5. Gently suggest professional help when appropriate for serious mental health concerns
                    6. Maintain appropriate boundaries - you're supportive but not a replacement for professional therapy

                    Guidelines for your responses:
                    - Use warm, understanding language
                    - Acknowledge their pain and validate their feelings
                    - Ask thoughtful follow-up questions when appropriate
                    - Offer specific, actionable advice for moving forward
                    - Share insights about the healing process
                    - Encourage self-compassion and patience
                    - Remind them that healing takes time
                    - Focus on their strength and resilience
                    - If someone mentions self-harm or severe depression, gently encourage them to seek professional help

                    Remember: You're here to provide comfort, guidance, and hope during a difficult time."""
    full_conversation = request.history + [
        {"role": "user", "content": request.message}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt}
        ] + full_conversation,
        temperature=0.7,
        max_tokens=300,
    )

    reply = response.choices[0].message.content
    return {"reply": reply}
