# Property Management Automation System

## Purpose
Automates property matching, commission calculations, transaction processing,
exception reporting, and operational summaries.

## Tech
- Python
- Pandas
- SQLite
- SQL
- Pytest
- Logging

## Workflow
1. Load property and customer-request CSV files.
2. Validate mandatory fields and numerical values.
3. Isolate invalid customer requests.
4. Match eligible available properties.
5. Rank matches with a documented score.
6. Calculate commission.
7. Save completed transactions.
8. Mark matched properties unavailable.
9. Create CSV reports and system logs.

## Run
python app.py

## Test
pytest -v

## Outputs
- matched_properties.csv
- exceptions.csv
- daily_summary.csv
- property_system.log

## Limitations
The application uses sample data and rule-based matching.
It does not connect to external property platforms or send live communications.
