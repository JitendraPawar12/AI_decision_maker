import re


def validate_and_normalize_product(product: str) -> str:
    if not isinstance(product, str):
        raise ValueError("Product name must be a text value.")

    normalized = product.strip()
    normalized = re.sub(r"\s{2,}", " ", normalized)

    if len(normalized) == 0:
        raise ValueError("Product name cannot be empty.")

    if len(normalized) < 3:
        raise ValueError("Product name must be at least 3 characters.")

    if normalized.isdigit():
        raise ValueError("Product name cannot be numeric only.")

    return normalized
