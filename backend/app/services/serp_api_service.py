import json
import re
from typing import Dict, List, Optional, Tuple

import requests
from requests import RequestException

from app.models.listing import Listing
import app.utils.env as env

SERPAPI_URL = "https://serpapi.com/search.json"
INDIAN_MAJOR_SITES = ["amazon", "flipkart", "myntra", "jiomart", "snapdeal", "tatacliq"]
INDIAN_LOCAL_MARKET_SITES = ["facebook", "olx", "quikr"]
SALE_KEYWORDS: Dict[str, str] = {
    "big billion": "Flipkart Big Billion Days",
    "great indian festival": "Flipkart Great Indian Festival",
    "diwali sale": "Diwali sale",
    "prime day": "Amazon Prime Day",
    "flipkart sale": "Flipkart Sale",
    "amazon sale": "Amazon Sale",
    "festive sale": "Festive Sale",
    "india sale": "India sale",
    "sale event": "Sale event",
}

MAJOR_SITE_NAMES = set(INDIAN_MAJOR_SITES)
LOCAL_MARKET_SITE_NAMES = set(INDIAN_LOCAL_MARKET_SITES)


def normalize_text(text: str) -> str:
    return str(text or "").strip().lower()


def extract_link(item: dict) -> str:
    return str(
        item.get("link")
        or item.get("product_link")
        or item.get("click_url")
        or item.get("url")
        or item.get("visible_link")
        or item.get("shopping_url")
        or item.get("source")
        or item.get("store")
        or ""
    ).strip()


def get_price_from_value(value) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("raw", "value", "displayed_price", "price", "amount"):
            nested = value.get(key)
            if nested:
                nested_str = get_price_from_value(nested)
                if nested_str:
                    return nested_str
        return None
    return str(value)


def classify_site(title: str, seller: str, source: str, link: str) -> str:
    normalized = normalize_text(f"{title} {seller} {source} {link}")
    if "flipkart" in normalized or "flipkart.com" in normalized:
        return "Flipkart"
    if "amazon" in normalized or "amazon.in" in normalized or "amazon.co.in" in normalized:
        return "Amazon"
    if "myntra" in normalized or "myntra.com" in normalized:
        return "Myntra"
    if "jiomart" in normalized or "jiomart.com" in normalized:
        return "JioMart"
    if "snapdeal" in normalized or "snapdeal.com" in normalized:
        return "Snapdeal"
    if "tatacliq" in normalized or "tata cliq" in normalized or "tatacliq.com" in normalized:
        return "TataCliq"
    if "facebook" in normalized or "marketplace" in normalized:
        return "Facebook Marketplace"
    if "olx" in normalized or "olx.in" in normalized:
        return "OLX"
    if "quikr" in normalized or "quikr.com" in normalized:
        return "Quikr"
    if "google" in normalized and "shopping" in normalized:
        return "Google Shopping"
    return "Other"


def is_relevant_site(site: str, link: str) -> bool:
    normalized = normalize_text(f"{site} {link}")
    relevant_patterns = MAJOR_SITE_NAMES | LOCAL_MARKET_SITE_NAMES | {
        "amazon.co.in",
        "flipkart.com",
        "myntra.com",
        "jiomart.com",
        "snapdeal.com",
        "tatacliq.com",
        "facebook.com",
        "olx.in",
        "quikr.com",
    }
    return any(pattern in normalized for pattern in relevant_patterns)


def is_major_site(listing: Listing) -> bool:
    normalized_site = normalize_text(listing.site)
    if normalized_site in MAJOR_SITE_NAMES:
        return True

    normalized_text = normalize_text(f"{listing.title} {listing.seller} {listing.source}")
    return any(name in normalized_text for name in MAJOR_SITE_NAMES)


def is_local_market_site(listing: Listing) -> bool:
    normalized_site = normalize_text(listing.site)
    if normalized_site in LOCAL_MARKET_SITE_NAMES:
        return True

    normalized_text = normalize_text(f"{listing.title} {listing.seller} {listing.source}")
    return any(name in normalized_text for name in LOCAL_MARKET_SITE_NAMES)


def detect_sale_event(listings: List[Listing]) -> Optional[str]:
    found_events = set()
    for listing in listings:
        text = normalize_text(f"{listing.title} {listing.seller} {listing.source}")
        for keyword, label in SALE_KEYWORDS.items():
            if keyword in text:
                found_events.add(label)
    return " | ".join(sorted(found_events)) if found_events else None


def parse_price(price_text) -> Optional[float]:
    raw_value = get_price_from_value(price_text)
    if not raw_value:
        return None

    cleaned = (
        raw_value
        .replace("$", "")
        .replace("₹", "")
        .replace("Rs", "")
        .replace("INR", "")
        .replace(",", "")
        .strip()
    )
    match = re.search(r"\d+(?:\.\d+)?", cleaned)
    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None


def parse_shopping_results(raw_data: dict) -> List[Listing]:
    results = raw_data.get("shopping_results") or raw_data.get("inline_shopping_results") or raw_data.get("results") or []
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
        link = extract_link(item)
        source = item.get("source") or item.get("link") or "SerpAPI"
        site = classify_site(title, seller, source, link)

        if not is_relevant_site(site, link):
            continue

        listings.append(
            Listing(
                title=title,
                price=price,
                seller=str(seller),
                source=str(source),
                site=site,
                link=link,
            )
        )

    return listings


def fetch_shopping_listings(product_name: str) -> Tuple[List[Listing], Optional[str], List[Listing], List[Listing], List[Listing]]:
    if not env.settings or not env.settings.SERP_API_KEY:
        raise ValueError("SERP_API_KEY is required. Set it in the environment or .env file.")

    params = {
        "engine": "google_shopping",
        "q": product_name,
        "api_key": env.settings.SERP_API_KEY,
        "hl": "en",
        "gl": "IN",
        "google_domain": "google.co.in",
        "num": "25",
    }

    try:
        response = requests.get(SERPAPI_URL, params=params, timeout=30)
        response.raise_for_status()
        raw_data = response.json()
    except RequestException as error:
        raise ValueError(f"SerpAPI request failed: {error}")
    except json.JSONDecodeError:
        raise ValueError("Failed to decode SerpAPI response.")

    listings = parse_shopping_results(raw_data)
    sale_event = detect_sale_event(listings)
    major_site_listings = [listing for listing in listings if is_major_site(listing)]
    local_market_listings = [listing for listing in listings if is_local_market_site(listing) and not is_major_site(listing)]
    other_listings = [listing for listing in listings if listing not in major_site_listings and listing not in local_market_listings]
    return listings, sale_event, major_site_listings, local_market_listings, other_listings
