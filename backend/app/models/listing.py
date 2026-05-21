from typing import Optional

from pydantic import BaseModel


class Listing(BaseModel):
    title: str
    price: float
    seller: str
    source: str
    site: str
    link: Optional[str] = None
