import os
from datetime import date, timedelta
from typing import Type

from crewai.tools import BaseTool
from exa_py import Exa
from pydantic import BaseModel, Field


class ExaSearchInput(BaseModel):
    query: str = Field(..., description="Search query for finding AI news articles")


class LimitedExaTool(BaseTool):
    name: str = "search_ai_news"
    description: str = (
        "Search for recent AI news articles. Returns up to 4 results, "
        "each with: headline, URL, published date, and a short snippet."
    )
    args_schema: Type[BaseModel] = ExaSearchInput

    def _run(self, query: str) -> str:
        exa = Exa(api_key=os.getenv("EXA_API_KEY"))
        week_ago = (date.today() - timedelta(days=7)).isoformat()

        try:
            response = exa.search_and_contents(
                query,
                num_results=4,
                text={"max_characters": 350},  # hard cap: ~88 tokens per result
                start_published_date=week_ago,
            )
        except Exception as e:
            return f"Search failed: {e}"

        if not response.results:
            return "No results found for this query."

        parts = []
        for r in response.results:
            snippet = (r.text or "").strip()[:350]
            pub = getattr(r, "published_date", "unknown date")
            parts.append(
                f"Headline: {r.title}\nURL: {r.url}\nDate: {pub}\nSnippet: {snippet}"
            )

        return "\n\n---\n\n".join(parts)
