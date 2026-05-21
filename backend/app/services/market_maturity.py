import statistics
from typing import List

from app.models.listing import Listing
from app.utils.schemas import MarketMaturitySchema


def compute_market_maturity(listings: List[Listing]) -> MarketMaturitySchema:
    if not listings:
        raise ValueError("Unable to compute market maturity for an empty listing set.")

    prices = [listing.price for listing in listings]
    unique_sellers = {listing.seller for listing in listings if listing.seller}
    listing_count = len(prices)
    seller_count = len(unique_sellers)
    min_price = min(prices)
    max_price = max(prices)
    average_price = sum(prices) / listing_count
    median_price = statistics.median(prices)
    price_spread = max_price - min_price

    is_mature = (
        listing_count >= 4
        and seller_count >= 3
        and price_spread >= max(5.0, average_price * 0.10)
    )

    return MarketMaturitySchema(
        seller_count=seller_count,
        listing_count=listing_count,
        price_spread=price_spread,
        average_price=round(average_price, 2),
        median_price=round(median_price, 2),
        is_mature=is_mature,
    )
