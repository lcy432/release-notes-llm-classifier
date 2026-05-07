import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"   # 关键：指向 DeepSeek 而不是 OpenAI
)

response = client.chat.completions.create(
    model="deepseek-chat",   # DeepSeek-V3 模型名
    messages=[
        {"role": "user", "content": "Reply with the word 'OK' and nothing else."}
    ],
    max_tokens=10
)

print(response.choices[0].message.content)