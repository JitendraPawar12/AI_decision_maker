from typing import Any

from app.models.listing import Listing
from app.utils.schemas import MarketMaturitySchema


def _normalize_confidence(score: float) -> float:
    return round(min(max(score, 0.0), 1.0), 2)


def evaluate_market_decision(listings: list[Listing], maturity: MarketMaturitySchema) -> dict[str, Any]:
    prices = sorted(listing.price for listing in listings)
    best_price = prices[0]
    average_price = maturity.average_price
    median_price = maturity.median_price
    listing_count = maturity.listing_count
    spread = maturity.price_spread

    decision = "WAIT"
    reason = "Insufficient market signal to recommend BUY at this time."
    confidence = 0.45

    if listing_count < 4 or not maturity.is_mature:
        reason = (
            "Market data is limited or immature. Wait for more seller listings and improved pricing visibility."
        )
        confidence = 0.42
    else:
        relative_to_median = (median_price - best_price) / median_price if median_price else 0.0
        if relative_to_median >= 0.15:
            decision = "BUY"
            reason = "Current best price is significantly below the median market price."
            confidence = 0.88
        elif relative_to_median >= 0.08:
            decision = "BUY"
            reason = "Current price is below the market median and presents a good opportunity."
            confidence = 0.76
        elif relative_to_median >= 0.03:
            decision = "WAIT"
            reason = "Price is only slightly below the median and could improve with more market visibility."
            confidence = 0.55
        else:
            decision = "WAIT"
            reason = "Price is near or above the expected market value, so waiting is safer."
            confidence = 0.60

    price_analysis = {
        "best_price": round(best_price, 2),
        "average_price": round(average_price, 2),
        "median_price": round(median_price, 2),
        "price_spread": round(spread, 2),
        "listing_count": listing_count,
        "price_position": "below_median" if best_price < median_price else "at_or_above_median",
    }

    return {
        "decision": decision,
        "confidence": _normalize_confidence(confidence),
        "reason": reason,
        "price_analysis": price_analysis,
    }
