import json
import openai
from typing import Any

import app.utils.env as env


def _fallback_explanation(product: str, decision: str, reason: str) -> str:
    return (
        f"Based on market maturity and price analysis for '{product}', the recommendation is {decision}. "
        f"Reason: {reason}"
    )


def generate_explanation(
    product: str,
    decision: str,
    confidence: float,
    reason: str,
    market_maturity: dict[str, Any],
    price_analysis: dict[str, Any],
) -> str:
    if not env.settings or not env.settings.OPENAI_API_KEY:
        return _fallback_explanation(product, decision, reason)

    openai.api_key = env.settings.OPENAI_API_KEY
    prompt = (
        "You are asked only to write a single JSON object with an explanation for a decision. "
        "Do not decide anything. Use the data exactly as provided. "
        "Output must be valid JSON with a single key named explanation. Example: {\"explanation\": \"...\"}."
    )

    system_message = {
        "role": "system",
        "content": "You are an explanation assistant. Explain why the decision was made using the supplied market data." 
    }
    user_message = {
        "role": "user",
        "content": json.dumps(
            {
                "product": product,
                "decision": decision,
                "confidence": confidence,
                "reason": reason,
                "market_maturity": market_maturity,
                "price_analysis": price_analysis,
            },
            indent=2,
        ),
    }

    try:
        completion = openai.ChatCompletion.create(
            model=env.settings.OPENAI_MODEL,
            messages=[system_message, {"role": "user", "content": prompt}, user_message],
            temperature=0.1,
            max_tokens=120,
        )
        raw_text = completion.choices[0].message.content.strip()
        explanation_payload = json.loads(raw_text)
        explanation = explanation_payload.get("explanation")
        if not explanation:
            return _fallback_explanation(product, decision, reason)
        return explanation
    except Exception:
        return _fallback_explanation(product, decision, reason)
