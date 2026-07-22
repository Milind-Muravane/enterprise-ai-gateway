from src.websearch.tavily import TavilySearch

search = TavilySearch()

result = search.search(
    "Latest AI news today"
)

print("=" * 70)

for item in result.results:

    print(item.title)
    print(item.url)
    print()
    print(item.content)
    print("-" * 70)