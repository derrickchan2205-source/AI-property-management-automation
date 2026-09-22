import logging
from pathlib import Path

from Database import create_tables, insert_transaction
from services.importer import load_csv
from services.validator import validate_properties, split_valid_requests
from services.matching_service import match_properties
from services.commission_service import calculate_commission

LOG_FILE = Path("logs/property_system.log")
OUTPUT_DIRECTORY = Path("output")

def configure_logging():
    LOG_FILE.parent.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

def run_automation():
    configure_logging()
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)

    logging.info("Property-management automation started")

    create_tables()

    properties = load_csv("data/properties.csv")
    requests = load_csv("data/customer_requests.csv")

    validate_properties(properties)

    valid_requests, invalid_requests = split_valid_requests(requests)

    invalid_requests.to_csv(
        OUTPUT_DIRECTORY / "exceptions.csv",
        index=False
    )

    matches = match_properties(properties, valid_requests)
    matches.to_csv(
        OUTPUT_DIRECTORY / "matched_properties.csv",
        index=False
    )

    completed_transactions = []

    for _, match in matches.iterrows():
        if match["match_status"] != "MATCHED":
            logging.warning(
                "No match found for request_id=%s",
                match["request_id"]
            )
            continue

        try:
            commission_rate = 0.02
            commission_amount = calculate_commission(
                match["price"],
                commission_rate
            )

            insert_transaction(
                request_id=match["request_id"],
                property_id=match["property_id"],
                sale_price=match["price"],
                commission_rate=commission_rate,
                commission_amount=commission_amount
            )

            completed_transactions.append({
                "request_id": match["request_id"],
                "property_id": match["property_id"],
                "sale_price": match["price"],
                "commission_rate": commission_rate,
                "commission_amount": commission_amount,
                "status": "COMPLETED"
            })

            logging.info(
                "Transaction completed: request_id=%s, property_id=%s",
                match["request_id"],
                match["property_id"]
            )

        except Exception:
            logging.exception(
                "Transaction failed: request_id=%s",
                match["request_id"]
            )

    summary = matches.groupby("match_status").size().reset_index(
        name="record_count"
    )

    summary.to_csv(
        OUTPUT_DIRECTORY / "daily_summary.csv",
        index=False
    )

    logging.info("Property-management automation completed")

if __name__ == "__main__":
    run_automation()