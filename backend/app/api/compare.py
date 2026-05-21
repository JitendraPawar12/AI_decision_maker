from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.services.product_existence import validate_and_normalize_product
from app.services.serp_api_service import fetch_shopping_listings
from app.services.market_maturity import compute_market_maturity
from app.services.decision_engine import evaluate_market_decision
from app.services.explain_service import generate_explanation
from app.utils.schemas import CompareRequest, CompareResponse

router = APIRouter(tags=["compare"])


@router.post("/compare", response_model=CompareResponse)
def compare_product(request: CompareRequest):
    try:
        product = validate_and_normalize_product(request.product)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    listings, sale_event, major_site_listings, local_market_listings, other_listings = fetch_shopping_listings(product)
    if not listings:
        raise HTTPException(status_code=404, detail="No shopping listings found for this product.")

    market_maturity = compute_market_maturity(listings)
    decision_output = evaluate_market_decision(listings, market_maturity)

    explanation = generate_explanation(
        product=product,
        decision=decision_output["decision"],
        confidence=decision_output["confidence"],
        reason=decision_output["reason"],
        market_maturity=market_maturity.dict(),
        price_analysis=decision_output["price_analysis"],
    )

    conclusion = (
        f"Final conclusion: {decision_output['decision']}. "
        f"Reason: {decision_output['reason']}"
    )

    response = {
        "product": product,
        "decision": decision_output["decision"],
        "confidence": decision_output["confidence"],
        "reason": decision_output["reason"],
        "conclusion": conclusion,
        "sale_event": sale_event,
        "major_site_listings": [listing.dict() for listing in major_site_listings],
        "local_market_listings": [listing.dict() for listing in local_market_listings],
        "other_listings": [listing.dict() for listing in other_listings],
        "listings": [listing.dict() for listing in listings],
        "market_maturity": market_maturity,
        "price_analysis": decision_output["price_analysis"],
        "explanation": explanation,
    }

    return response
