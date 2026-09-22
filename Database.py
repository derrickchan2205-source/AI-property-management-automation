import sqlite3
from pathlib import Path

DATABASE_PATH = Path("property_management.db")

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            property_id TEXT PRIMARY KEY,
            district TEXT NOT NULL,
            property_type TEXT NOT NULL,
            price REAL NOT NULL CHECK(price > 0),
            area_sqft REAL NOT NULL CHECK(area_sqft > 0),
            bedrooms INTEGER NOT NULL CHECK(bedrooms >= 0),
            available INTEGER NOT NULL DEFAULT 1
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS customer_requests (
            request_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            preferred_district TEXT NOT NULL,
            max_budget REAL NOT NULL CHECK(max_budget > 0),
            min_area_sqft REAL NOT NULL CHECK(min_area_sqft > 0),
            min_bedrooms INTEGER NOT NULL CHECK(min_bedrooms >= 0)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT NOT NULL,
            property_id TEXT NOT NULL,
            sale_price REAL NOT NULL,
            commission_rate REAL NOT NULL,
            commission_amount REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(request_id) REFERENCES customer_requests(request_id),
            FOREIGN KEY(property_id) REFERENCES properties(property_id)
        )
    """)

    connection.commit()
    connection.close()

def insert_transaction(
    request_id,
    property_id,
    sale_price,
    commission_rate,
    commission_amount,
    status="COMPLETED"
):
    connection = get_connection()

    try:
        connection.execute("BEGIN")

        connection.execute("""
            INSERT INTO transactions (
                request_id,
                property_id,
                sale_price,
                commission_rate,
                commission_amount,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            request_id,
            property_id,
            sale_price,
            commission_rate,
            commission_amount,
            status
        ))

        connection.execute("""
            UPDATE properties
            SET available = 0
            WHERE property_id = ?
        """, (property_id,))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()