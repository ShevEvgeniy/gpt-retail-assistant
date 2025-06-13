from fastapi import FastAPI, Query
from pydantic import BaseModel
from chunks import Chunk
import os

# Инициализация FastAPI
app = FastAPI()

# Создаём экземпляр Chunk (документ находится в той же папке)
chunk = Chunk(path_to_base="chunks_export.md")

# Модель запроса
class Question(BaseModel):
    query: str

# Роут для POST-запроса с телом
@app.post("/ask")
def ask_question(data: Question):
    answer = chunk.get_answer(query=data.query)
    return {"answer": answer}

# Роут для GET-запроса с параметром
@app.get("/ask")
def ask_question_get(query: str = Query(..., description="Вопрос клиента")):
    answer = chunk.get_answer(query=query)
    return {"answer": answer}
