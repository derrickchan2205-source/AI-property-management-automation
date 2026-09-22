from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Property:
    property_id: str
    district: str
    property_type: str
    price: Decimal
    area_sqft: float
    bedrooms: int
    available: bool