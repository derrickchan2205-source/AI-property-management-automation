from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CustomerRequest:
    request_id: str
    customer_name: str
    preferred_district: str
    max_budget: Decimal
    min_area_sqft: float
    min_bedrooms: int