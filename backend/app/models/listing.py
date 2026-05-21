from pydantic import BaseModel


class Listing(BaseModel):
    title: str
    price: float
    seller: str
    source: str
