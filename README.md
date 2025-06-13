# GPT Retail Assistant 🍣🤖

Интеллектуальный чат-бот-консультант для онлайн-магазина суши на базе Django + FastAPI + GPT-4o.

## 📌 Введение
Проект представляет собой интеграцию FastAPI-сервиса генерации ответов на естественном языке (с использованием GPT) с интерфейсом на Django. Пользователь может задавать вопросы в чате, а бот отвечает на основе документации и базы товаров (markdown-файл, превращённый в эмбеддинги).

Основной упор сделан на практическое применение GPT в электронной коммерции и консультациях.

## 📦 Возможности
- 💬 Чат-бот, отвечающий на основе содержимого `.md`-документа
- 🧠 Поддержка истории диалога (контекст сохраняется в localStorage)
- 🛒 Подсказки по товарам с активными ссылками
- 🔄 Кнопка "очистить диалог"
- 📂 Интеграция Django + FastAPI (через JS Fetch API)

---

## ⚙️ Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/ShevEvgeniy/gpt-retail-assistant.git
cd gpt-retail-assistant
```

### 2. Установка зависимостей Django
```bash
cd django_app
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Установка и запуск FastAPI-сервиса
```bash
cd ../fastapi_sushi
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requierments.txt
uvicorn main:app --port 5000
```

### 4. Настрой .env (пример в `.env_example`):
```
OPENAI_API_KEY=sk-...
```

---

## 💡 Пример использования
На странице `/dialog/` появляется чат, где можно:
- Задать вопрос о продукции
- Получить ответ, сгенерированный на основе `.md`-файла
- Перейти по ссылке на товар
- Очистить диалог кнопкой "🗑 Очистить"

---

## 🗂 Структура проекта
```
gpt-retail-assistant/
├── django_app/            # Django-приложение с шаблонами и каталогом
├── fastapi_sushi/         # FastAPI-сервис с GPT и FAISS
│   ├── chunks.py          # Обработка запроса и поиск по базе
│   └── main.py            # FastAPI endpoint
├── chunks_export.md       # Markdown база знаний
└── README.md
```

---

## 🚀 Технологии
- Django
- FastAPI
- OpenAI GPT-4o
- LangChain + FAISS
- AlpineJS + Marked.js

---

## 📎 Полезные команды
```bash
# Django
python manage.py runserver
python manage.py createsuperuser

# FastAPI
uvicorn main:app --port 5000
```

---

## 📢 Автор
[Evgeniy Shevchenko](https://github.com/ShevEvgeniy)

---

## 📃 Лицензия
Проект распространяется под MIT лицензией.
