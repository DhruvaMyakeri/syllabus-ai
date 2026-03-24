from backend.services.gemini_client import generate
from backend.utils.json_cleaner import extract_json

def generate_questions(topic):
    prompt = f"""
    Generate 5 exam questions.

    Return JSON:
    {{
      "questions": ["q1", "q2"]
    }}

    Topic:
    {topic}
    """

    result = generate(prompt)
    data = extract_json(result)

    return data.get("questions", []) if data else []