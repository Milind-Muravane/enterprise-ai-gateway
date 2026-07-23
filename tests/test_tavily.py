from src.websearch.tavily import TavilySearch

search = TavilySearch()

result = search.search(
    "Latest news in India protest today 23/07/2026"
)

print("=" * 70)

for item in result.results:

    print(item.title)
    print(item.url)
    print()
    print(item.content)
    print("-" * 70)