# python
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    sys.exit("ERROR: переменная окружения `OPENAI_API_KEY` не задана. Проверьте `.env` и имя ключа.")

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello, can you help me?"},
        ],
    )
except Exception as e:
    sys.exit(f"API error: {e}")

# Попытаться безопасно получить контент из разных возможных структур ответа
content = None
try:
    content = response.choices[0].message.content  # объект с атрибутом
except Exception:
    try:
        content = response.choices[0].message["content"]  # dict-подобная структура
    except Exception:
        # fallback — вывести весь ответ в читаемом виде
        try:
            content = response.model_dump_json(indent=2)
        except Exception:
            content = str(response)

print(content)