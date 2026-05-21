import json
import re
from typing import List, Optional

import requests
from requests import RequestException

from app.models.listing import Listing
import app.utils.env as env

SERPAPI_URL = "https://serpapi.com/search.json"


def parse_price(price_text: str) -> Optional[float]:
    if not price_text:
        return None

    cleaned = price_text.replace("$", "").replace(",", "").strip()
    match = re.search(r"\d+(?:\.\d+)?", cleaned)
    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None


def parse_shopping_results(raw_data: dict) -> List[Listing]:
    results = raw_data.get("shopping_results") or []
    listings: list[Listing] = []

    for item in results:
        if not isinstance(item, dict):
            continue

        price_text = item.get("price") or item.get("extracted_price") or item.get("displayed_price")
        price = parse_price(str(price_text))
        if price is None:
            continue

        title = item.get("title") or item.get("product_title") or "Unknown product"
        seller = item.get("source") or item.get("seller") or item.get("store") or "Unknown seller"
        source = item.get("source") or item.get("link") or "SerpAPI"

        listings.append(
            Listing(
                title=title,
                price=price,
                seller=str(seller),
                source=str(source),
            )
        )

    return listings


def fetch_shopping_listings(product_name: str) -> List[Listing]:
    if not env.settings or not env.settings.SERP_API_KEY:
        raise ValueError("SERP_API_KEY is required. Set it in the environment or .env file.")

    params = {
        "engine": "google_shopping",
        "q": product_name,
        "api_key": env.settings.SERP_API_KEY,
        "hl": "en",
        "gl": "us",
        "num": "20",
    }

    try:
        response = requests.get(SERPAPI_URL, params=params, timeout=15)
        response.raise_for_status()
        raw_data = response.json()
    except RequestException as error:
        raise ValueError(f"SerpAPI request failed: {error}")
    except json.JSONDecodeError:
        raise ValueError("Failed to decode SerpAPI response.")

    listings = parse_shopping_results(raw_data)
    return listings
