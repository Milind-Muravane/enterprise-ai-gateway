print("1. Script started")

from src.providers.factory import get_provider
from src.schemas import Provider

print("2. Imports successful")

provider = get_provider(Provider.GEMINI)

print("3. Provider created:", provider)

response = provider.generate(
    prompt="Who are you?",
    model="gemini-2.5-flash",
)

print("4. Response received")

print(response.answer)
print(response.latency_ms)