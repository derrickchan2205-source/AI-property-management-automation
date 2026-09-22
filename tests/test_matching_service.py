import pandas as pd

from services.matching_service import match_properties

def test_matching_returns_eligible_property():
    properties = pd.DataFrame([
        {
            "property_id": "P001",
            "district": "Sha Tin",
            "property_type": "Apartment",
            "price": 5800000,
            "area_sqft": 520,
            "bedrooms": 2,
            "available": True
        }
    ])

    requests = pd.DataFrame([
        {
            "request_id": "R001",
            "customer_name": "Alex Chan",
            "preferred_district": "Sha Tin",
            "max_budget": 6500000,
            "min_area_sqft": 500,
            "min_bedrooms": 2
        }
    ])

    result = match_properties(properties, requests)

    assert result.iloc[0]["match_status"] == "MATCHED"
    assert result.iloc[0]["property_id"] == "P001"

def test_matching_returns_no_match_when_budget_is_too_low():
    properties = pd.DataFrame([
        {
            "property_id": "P001",
            "district": "Sha Tin",
            "property_type": "Apartment",
            "price": 5800000,
            "area_sqft": 520,
            "bedrooms": 2,
            "available": True
        }
    ])

    requests = pd.DataFrame([
        {
            "request_id": "R002",
            "customer_name": "Jamie Wong",
            "preferred_district": "Sha Tin",
            "max_budget": 5000000,
            "min_area_sqft": 500,
            "min_bedrooms": 2
        }
    ])

    result = match_properties(properties, requests)

    assert result.iloc[0]["match_status"] == "NO_MATCH"