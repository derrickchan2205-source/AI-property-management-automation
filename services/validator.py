REQUIRED_PROPERTY_COLUMNS = {
    "property_id",
    "district",
    "property_type",
    "price",
    "area_sqft",
    "bedrooms",
    "available"
}

REQUIRED_REQUEST_COLUMNS = {
    "request_id",
    "customer_name",
    "preferred_district",
    "max_budget",
    "min_area_sqft",
    "min_bedrooms"
}

def validate_required_columns(dataframe, required_columns):
    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

def validate_properties(dataframe):
    validate_required_columns(dataframe, REQUIRED_PROPERTY_COLUMNS)

    errors = []

    if dataframe["property_id"].duplicated().any():
        errors.append("Duplicate property_id found")

    if dataframe["price"].isna().any() or (dataframe["price"] <= 0).any():
        errors.append("Price must be present and greater than zero")

    if dataframe["area_sqft"].isna().any() or (dataframe["area_sqft"] <= 0).any():
        errors.append("Area must be present and greater than zero")

    if dataframe["bedrooms"].isna().any() or (dataframe["bedrooms"] < 0).any():
        errors.append("Bedrooms must be zero or greater")

    if errors:
        raise ValueError("; ".join(errors))

def split_valid_requests(dataframe):
    validate_required_columns(dataframe, REQUIRED_REQUEST_COLUMNS)

    valid_mask = (
        dataframe["request_id"].notna()
        & dataframe["customer_name"].notna()
        & dataframe["preferred_district"].notna()
        & dataframe["max_budget"].notna()
        & dataframe["min_area_sqft"].notna()
        & dataframe["min_bedrooms"].notna()
        & (dataframe["max_budget"] > 0)
        & (dataframe["min_area_sqft"] > 0)
        & (dataframe["min_bedrooms"] >= 0)
    )

    valid_requests = dataframe[valid_mask].copy()
    invalid_requests = dataframe[~valid_mask].copy()

    return valid_requests, invalid_requests