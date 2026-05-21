from datetime import datetime
from typing import Any

from app.models.listing import Listing
from app.utils.schemas import MarketMaturitySchema


def _normalize_confidence(score: float) -> float:
    return round(min(max(score, 0.0), 1.0), 2)


def get_upcoming_festivals() -> list[dict[str, str]]:
    """Predict upcoming Indian festivals and sale events based on current date."""
    today = datetime.now()
    month = today.month
    
    festivals = []
    
    # Big Billion Days (Sept-Oct)
    if month in [9, 10]:
        festivals.append({
            "name": "Flipkart Big Billion Days",
            "month": "Sept-Oct",
            "discount": "Up to 70% off on selected items"
        })
    
    # Great Indian Festival (Aug-Sept)
    if month in [8, 9]:
        festivals.append({
            "name": "Flipkart Great Indian Festival",
            "month": "Aug-Sept",
            "discount": "Up to 75% off on electronics & home"
        })
    
    # Diwali sale (Oct-Nov)
    if month in [10, 11]:
        festivals.append({
            "name": "Diwali Sale (Amazon & Flipkart)",
            "month": "Oct-Nov",
            "discount": "Up to 50% off + extra discounts"
        })
    
    # Amazon Prime Day (July-Aug)
    if month in [7, 8]:
        festivals.append({
            "name": "Amazon Prime Day",
            "month": "July-Aug",
            "discount": "Exclusive deals for Prime members"
        })
    
    # Christmas & New Year (Dec)
    if month == 12:
        festivals.append({
            "name": "Christmas & New Year Sale",
            "month": "Dec",
            "discount": "Up to 70% off on multiple categories"
        })
    
    # Holi sale (March)
    if month == 3:
        festivals.append({
            "name": "Holi Sale",
            "month": "March",
            "discount": "Up to 60% off on all categories"
        })
    
    return festivals


def evaluate_market_decision(listings: list[Listing], maturity: MarketMaturitySchema) -> dict[str, Any]:
    if not listings:
        return {
            "decision": "WAIT",
            "confidence": 0.3,
            "reason": "No listings found for this product.",
            "price_analysis": {},
            "upcoming_festivals": get_upcoming_festivals(),
        }
    
    prices = sorted(listing.price for listing in listings)
    best_price = prices[0]
    average_price = maturity.average_price
    median_price = maturity.median_price
    listing_count = maturity.listing_count
    spread = maturity.price_spread

    decision = "BUY"
    reason = ""
    confidence = 0.65
    upcoming_festivals = get_upcoming_festivals()

    # If very few listings, just check if price seems good
    if listing_count < 3:
        if best_price < average_price * 0.9:
            decision = "BUY"
            reason = f"Good price found at ₹{best_price}. Limited options available, but this offer seems competitive."
            confidence = 0.70
        elif best_price < average_price:
            decision = "BUY"
            reason = f"Current price at ₹{best_price} is below average. Reasonable option to purchase."
            confidence = 0.62
        else:
            if upcoming_festivals:
                decision = "INFORM"
                festival_names = ", ".join(f["name"] for f in upcoming_festivals)
                reason = f"Current price is at market rate. {festival_names} coming soon with potential discounts."
                confidence = 0.58
            else:
                decision = "WAIT"
                reason = "Current price is at or above average. Consider waiting for better deals."
                confidence = 0.55
    else:
        # Market is more mature with sufficient data
        relative_to_median = (median_price - best_price) / median_price if median_price else 0.0
        
        if relative_to_median >= 0.15:
            decision = "BUY"
            reason = "Excellent deal! Current best price is significantly below the median market price."
            confidence = 0.90
        elif relative_to_median >= 0.08:
            decision = "BUY"
            reason = "Good value! Current price is below market median and presents a solid opportunity."
            confidence = 0.78
        elif relative_to_median >= 0.03:
            if upcoming_festivals:
                decision = "INFORM"
                festival_names = ", ".join(f["name"] for f in upcoming_festivals)
                reason = f"Price is near median. {festival_names} approaching - better discounts expected."
                confidence = 0.65
            else:
                decision = "WAIT"
                reason = "Price is only slightly below median. Waiting might yield better offers."
                confidence = 0.58
        else:
            if upcoming_festivals and spread > average_price * 0.05:
                decision = "INFORM"
                festival_names = ", ".join(f["name"] for f in upcoming_festivals)
                reason = f"Price at market rate. {festival_names} could bring 20-50% discounts based on past patterns."
                confidence = 0.62
            else:
                decision = "WAIT"
                reason = "Price is at or above expected market value. Waiting for discounts is recommended."
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
        "upcoming_festivals": upcoming_festivals,
    }
