import requests
from config import settings

SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"


def chat_completion(messages, model="deepseek-ai/DeepSeek-V3.2") -> str:
    if not settings.SILICONFLOW_API_KEY:
        raise RuntimeError("未检测到 SILICONFLOW_API_KEY，请检查 Starji1/.env")

    headers = {
        "Authorization": f"Bearer {settings.SILICONFLOW_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.8,
        "max_tokens": 2048,
        "stream": False,
    }

    resp = requests.post(
        SILICONFLOW_BASE_URL,
        headers=headers,
        json=payload,
        timeout=300,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]
