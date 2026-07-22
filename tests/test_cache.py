from src.cache.chroma import ChromaCache

cache = ChromaCache()

cache.clear()

cache.add(

    question="What is baggage allowance?",

    answer="Passengers may carry 15 kg of checked baggage."

)

results = cache.search(

    "Tell me the baggage limit."

)

print(results)