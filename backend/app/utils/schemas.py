from pydantic import BaseModel, Field
from typing import List


class CompareRequest(BaseModel):
    product: str = Field(..., min_length=1, description="Product name to compare.")


class ListingSchema(BaseModel):
    title: str
    price: float
    seller: str
    source: str


class MarketMaturitySchema(BaseModel):
    seller_count: int
    listing_count: int
    price_spread: float
    average_price: float
    median_price: float
    is_mature: bool


class PriceAnalysisSchema(BaseModel):
    best_price: float
    average_price: float
    median_price: float
    price_spread: float
    listing_count: int
    price_position: str


class CompareResponse(BaseModel):
    product: str
    decision: str
    confidence: float
    reason: str
    conclusion: str
    listings: List[ListingSchema]
    market_maturity: MarketMaturitySchema
    price_analysis: PriceAnalysisSchema
    explanation: str
