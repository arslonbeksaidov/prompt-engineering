# ollama_client.py

import requests

def ollama_chat(base_url, model, system_prompt, user_prompt, max_tokens=384, temperature=0.2, top_p=0.9):

    url = f"{base_url}/api/chat"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,  # ← MUHIM
        "options": {
            "num_predict": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
    }

    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()

    data = r.json()

    if isinstance(data, dict) and "message" in data:
        return data["message"].get("content", "").strip()

    return str(data)
