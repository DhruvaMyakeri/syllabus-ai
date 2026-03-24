from backend.services.gemini_client import generate
from backend.utils.json_cleaner import extract_json

def analyze_comments(comments):
    if not comments:
        return 0

    prompt = f"""
    Analyze sentiment of these comments.

    Return JSON:
    {{
      "score": number between -1 and 1
    }}

    Comments:
    {" ".join(comments)}
    """

    result = generate(prompt)
    data = extract_json(result)

    return data.get("score", 0) if data else 0