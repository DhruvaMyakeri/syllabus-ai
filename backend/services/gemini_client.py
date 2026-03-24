from google import genai

API_KEYS = [
    ""
]

current_key_index = 0


def get_client():
    global current_key_index
    return genai.Client(api_key=API_KEYS[current_key_index])


def switch_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(API_KEYS)


def generate(prompt: str) -> str:
    for _ in range(len(API_KEYS)):
        try:
            client = get_client()

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text if response.text else str(response)

        except Exception as e:
            print("Gemini key failed, switching...")
            switch_key()

    raise Exception("All Gemini API keys exhausted")