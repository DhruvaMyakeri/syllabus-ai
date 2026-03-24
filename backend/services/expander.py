from backend.services.gemini_client import generate
from backend.utils.json_cleaner import extract_json

def fallback_expand(topics):
    result = []

    for t in topics:
        result.append({
            "name": t,
            "subtopics": [
                f"{t} basics",
                f"{t} examples",
                f"{t} problems",
                f"{t} applications"
            ]
        })

    return result


def expand_all(topics):
    try:
        prompt = f"""
        For each topic, generate max 4 important subtopics.

        Return JSON:
        {{
          "topics": [
            {{
              "name": "topic",
              "subtopics": []
            }}
          ]
        }}

        Topics:
        {topics}
        """

        result = generate(prompt)
        data = extract_json(result)

        if data and "topics" in data:
            return data["topics"]

    except Exception:
        print("Expander fallback used")

    return fallback_expand(topics)