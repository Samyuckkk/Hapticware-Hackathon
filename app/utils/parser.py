import json

def safe_parse_llm_output(text: str):
    try:
        return json.loads(text)
    except:
        # try fixing common issues
        text = text.replace("```json", "").replace("```", "")
        return json.loads(text)