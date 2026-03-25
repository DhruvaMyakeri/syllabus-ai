import json
import re
from .gemini_client import call_gemini

def parse_syllabus(syllabus_text: str) -> list:
    prompt = f"""You are an expert academic syllabus analyzer.
Return ONLY JSON.
Ensure domain correctness.
Do not hallucinate.
Do not include markdown.

Analyze the following syllabus text, interpret meaning (NOT just splitting strings), 
group concepts logically, and identify the domain context.
Remove noise like unit labels or formatting artifacts ("Unit 1", "Numerical on", etc.).
Fix ambiguity (e.g., 'Reno' -> 'TCP Reno', 'Fragmentation' -> 'IP Fragmentation', 'Addressing' -> 'IP Addressing').
Extract topics and meaningful subtopics. DO NOT output generic subtopics like 'basics', 'examples', 'applications'.
ONLY output real academic concepts.

Output format must be strictly a JSON list of objects without markdown backticks:
[
  {{
    "topic": "Topic Name",
    "subtopics": ["Subtopic 1", "Subtopic 2"]
  }}
]

Syllabus text:
{syllabus_text}
"""
    
    response_text = call_gemini(prompt)
    
    # Clean up markdown if any
    clean_text = re.sub(r'```json\s*', '', response_text)
    clean_text = re.sub(r'```\s*', '', clean_text)
    clean_text = clean_text.strip()
    
    try:
        data = json.loads(clean_text)
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {clean_text}")
        raise ValueError("Failed to parse Gemini response as JSON")