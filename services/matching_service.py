import pandas as pd

def calculate_match_score(property_row, request_row):
    budget_score = 1 - (property_row["price"] / request_row["max_budget"])
    area_score = property_row["area_sqft"] / request_row["min_area_sqft"]
    bedroom_score = property_row["bedrooms"] / max(request_row["min_bedrooms"], 1)

    return round(
        (budget_score * 0.50)
        + (area_score * 0.30)
        + (bedroom_score * 0.20),
        4
    )

def match_properties(properties_df, requests_df):
    all_matches = []

    available_properties = properties_df[
        properties_df["available"].astype(str).str.lower() == "true"
    ].copy()

    for _, request in requests_df.iterrows():
        matches = available_properties[
            (available_properties["district"].str.lower() ==
             request["preferred_district"].lower())
            & (available_properties["price"] <= request["max_budget"])
            & (available_properties["area_sqft"] >= request["min_area_sqft"])
            & (available_properties["bedrooms"] >= request["min_bedrooms"])
        ].copy()

        if matches.empty:
            all_matches.append({
                "request_id": request["request_id"],
                "customer_name": request["customer_name"],
                "property_id": None,
                "match_status": "NO_MATCH",
                "match_score": None
            })
            continue

        matches["match_score"] = matches.apply(
            lambda property_row: calculate_match_score(property_row, request),
            axis=1
        )

        matches = matches.sort_values(
            by=["match_score", "price"],
            ascending=[False, True]
        )

        best_match = matches.iloc[0]

        all_matches.append({
            "request_id": request["request_id"],
            "customer_name": request["customer_name"],
            "property_id": best_match["property_id"],
            "district": best_match["district"],
            "property_type": best_match["property_type"],
            "price": best_match["price"],
            "area_sqft": best_match["area_sqft"],
            "bedrooms": best_match["bedrooms"],
            "match_status": "MATCHED",
            "match_score": best_match["match_score"]
        })

    return pd.DataFrame(all_matches)