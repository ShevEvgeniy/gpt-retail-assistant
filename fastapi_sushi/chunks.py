from openai import OpenAI
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_openai import OpenAIEmbeddings
import os
import re
from typing import List

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Системный промпт
DEFAULT_SYSTEM_PROMPT = (
    "Ты — консультант в компании СушиShop. Отвечай на вопросы клиентов ТОЛЬКО на основе документа с информацией. "
    "Не придумывай ничего от себя, не пиши, что ты искусственный интеллект. Не упоминай документ с информацией.\n\n"
    "Если клиент спрашивает про скидки, акции, товары со сниженной ценой, или говорит: «что подешевле», "
    "обязательно предложи из раздела с товарами по акции. Укажи конкретные названия и ссылки на них.\n\n"
    "Если среди документов найдется подходящий товар, обязательно включи его название и ссылку в ответ."
)

class Chunk:
    def __init__(self, path_to_base: str = "chunks_export.md"):
        with open(path_to_base, 'r', encoding='utf-8') as file:
            document = file.read()

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]

        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_chunks = splitter.split_text(document)

        for chunk in md_chunks:
            match = re.search(r']\(([^)]+)\)', chunk.page_content)
            if match:
                chunk.metadata['url'] = match.group(1)
            chunk.page_content = f"{chunk.metadata.get('Header 2', '')}\n{chunk.page_content}"

        self.docs = md_chunks
        self.texts = [doc.page_content for doc in md_chunks]
        self.db = FAISS.from_texts(
            self.texts,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key),
            metadatas=[doc.metadata for doc in md_chunks]
        )

    async def get_async_answer_text(self, query: str, last_messages: List[dict] = None, system: str = DEFAULT_SYSTEM_PROMPT):
        docs = self.db.similarity_search(query, k=4)
        message_content = "\n".join([doc.page_content for doc in docs])

        messages = []
        messages.append({"role": "system", "content": system})

        if last_messages:
            messages.extend(last_messages)

        # Добавляем новый запрос, обернутый в инструкцию
        messages.append({
            "role": "user",
            "content": f"Ответь на вопрос клиента только на основе документа с информацией. "
                       f"Не упоминай документ с информацией для ответа клиенту в ответе. "
                       f"Документ с информацией для ответа клиенту: ```{message_content}```\n"
                       f"Вопрос клиента: \n{query}"
        })

        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
        )

        for part in stream:
            delta = part.choices[0].delta
            if delta and delta.content:
                yield delta.content
