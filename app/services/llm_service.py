import requests
import os

API_KEY = os.getnev("OPENROUTER_API_KEY")

def extract_invoice_data(raw_text: str):
    print("API KEY:", API_KEY)

    prompt = f"Extract invoice data from this text:\n{raw_text}"

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Invoice App",
        },
        json={
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [{"role": "user", "content": prompt}],
        },
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    try:
        data = response.json()
    except:
        print("JSON PARSE ERROR")
        raise Exception("Invalid JSON response")

    if "choices" not in data:
        print("LLM ERROR:", data)
        raise Exception("LLM API failed")

    return data["choices"][0]["message"]["content"]