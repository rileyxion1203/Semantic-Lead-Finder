"""
exa_search.py
Real-time company search using Exa API.
"""

import os
from exa_py import Exa


def get_client() -> Exa:
    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        raise ValueError("EXA_API_KEY not set in .env")
    return Exa(api_key=api_key)


def search_companies(query: str, num_results: int = 10) -> list[dict]:
    exa = get_client()

    prefixed_query = f"company that {query}"

    response = exa.search(
        prefixed_query,
        num_results=num_results,
        type="neural",
        category="company",
        contents={
            "text": {"max_characters": 800},
            "highlights": {
                "num_sentences": 2,
                "highlights_per_url": 1,
            },
        },
    )

    results = []
    for i, r in enumerate(response.results):
        highlight = ""
        if r.highlights:
            highlight = r.highlights[0]

        results.append({
            "rank": i + 1,
            "title": r.title or "—",
            "url": r.url or "",
            "highlight": highlight,
            "published_date": r.published_date or "",
            "id": r.id,
        })

    return results
