from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from chunks import Chunk
import os

app = FastAPI()

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели запроса
class DialogMessage(BaseModel):
    content: str
    role: str

class Request(BaseModel):
    text: str
    messages: List[DialogMessage] = []

# Загружаем базу
chunk = Chunk(path_to_base=os.path.join(os.path.dirname(__file__), "chunks_export.md"))

@app.post("/api/get_answer")
async def get_answer(request: Request):
    print("Получен запрос:")
    print("Текст:", request.text)
    print("История:")
    for m in request.messages:
        print(f"{m.role}: {m.content}")

    full_answer = ""
    async for part in chunk.get_async_answer_text(query=request.text, last_messages=request.messages):
        full_answer += part

    return {"answer": full_answer}
