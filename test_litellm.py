from litellm import completion
from src.config import settings

response = completion(
    model="gemini/gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": "Say hello."
        }
    ],
    api_key=settings.gemini_api_key,
)

print(response)