"""
generate_data.py
-----------------
Generates a synthetic SQLite database (customer_success.db) that mimics
a SaaS company's customer success data: customers, support tickets,
satisfaction/NPS surveys, contract renewals, and product usage logs.

Run this once before using the KPI/chart scripts:
    python data/generate_data.py
"""

import argparse
import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

DB_PATH = Path(__file__).resolve().parent.parent / "customer_success.db"

DEFAULT_NUM_CUSTOMERS = 150
PLANS = ["Basic", "Pro", "Enterprise"]
INDUSTRIES = ["Retail", "Healthcare", "Finance", "Education", "Technology", "Manufacturing"]
TICKET_CATEGORIES = ["Bug", "Billing", "Feature Request", "Complaint", "How-To", "Onboarding"]
FEATURES = ["Dashboard", "Reporting", "API", "Integrations", "Mobile App", "Automation"]

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)


def random_date(start=START_DATE, end=END_DATE):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def build_schema(conn):
    cur = conn.cursor()
    cur.executescript(
        """
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS tickets;
        DROP TABLE IF EXISTS surveys;
        DROP TABLE IF EXISTS renewals;
        DROP TABLE IF EXISTS usage_logs;

        CREATE TABLE customers (
            customer_id   INTEGER PRIMARY KEY,
            name          TEXT NOT NULL,
            industry      TEXT NOT NULL,
            plan          TEXT NOT NULL,
            signup_date   TEXT NOT NULL
        );

        CREATE TABLE tickets (
            ticket_id     INTEGER PRIMARY KEY,
            customer_id   INTEGER NOT NULL,
            category      TEXT NOT NULL,
            created_at    TEXT NOT NULL,
            first_response_at TEXT,
            closed_at     TEXT,
            status        TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE surveys (
            survey_id       INTEGER PRIMARY KEY,
            customer_id     INTEGER NOT NULL,
            survey_date     TEXT NOT NULL,
            satisfaction_score INTEGER NOT NULL, -- 1-5 (CSAT)
            nps_score       INTEGER NOT NULL,    -- 0-10
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE renewals (
            renewal_id      INTEGER PRIMARY KEY,
            customer_id     INTEGER NOT NULL,
            contract_start  TEXT NOT NULL,
            contract_end    TEXT NOT NULL,
            renewed         INTEGER NOT NULL, -- 1 = renewed, 0 = churned
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE usage_logs (
            usage_id        INTEGER PRIMARY KEY,
            customer_id     INTEGER NOT NULL,
            usage_date      TEXT NOT NULL,
            feature         TEXT NOT NULL,
            usage_count     INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
        """
    )
    conn.commit()


def seed_customers(conn, num_customers):
    rows = []
    for cid in range(1, num_customers + 1):
        signup = random_date(START_DATE, END_DATE - timedelta(days=30))
        rows.append(
            (
                cid,
                fake.company(),
                random.choice(INDUSTRIES),
                random.choice(PLANS),
                signup.strftime("%Y-%m-%d"),
            )
        )
    conn.executemany(
        "INSERT INTO customers (customer_id, name, industry, plan, signup_date) VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    return rows


def seed_tickets(conn, customers):
    rows = []
    ticket_id = 1
    for cid, *_ in customers:
        num_tickets = random.randint(0, 12)
        for _ in range(num_tickets):
            created = random_date()
            # response time: mostly fast, occasional slow outliers
            response_hours = max(0.5, random.gauss(6, 5))
            first_response = created + timedelta(hours=response_hours)

            status = random.choices(["Closed", "Open"], weights=[0.85, 0.15])[0]
            closed_at = None
            if status == "Closed":
                resolution_hours = max(response_hours, random.gauss(30, 20))
                closed_at = (created + timedelta(hours=resolution_hours)).strftime("%Y-%m-%d %H:%M:%S")

            category = random.choices(
                TICKET_CATEGORIES, weights=[0.2, 0.15, 0.15, 0.2, 0.2, 0.1]
            )[0]

            rows.append(
                (
                    ticket_id,
                    cid,
                    category,
                    created.strftime("%Y-%m-%d %H:%M:%S"),
                    first_response.strftime("%Y-%m-%d %H:%M:%S"),
                    closed_at,
                    status,
                )
            )
            ticket_id += 1

    conn.executemany(
        """INSERT INTO tickets
           (ticket_id, customer_id, category, created_at, first_response_at, closed_at, status)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()


def seed_surveys(conn, customers):
    rows = []
    survey_id = 1
    for cid, *_ in customers:
        num_surveys = random.randint(1, 6)
        # give each customer a "sentiment bias" so trends look realistic
        bias = random.uniform(-1, 1)
        for _ in range(num_surveys):
            survey_date = random_date()
            satisfaction = min(5, max(1, round(random.gauss(3.7 + bias * 0.6, 0.9))))
            nps = min(10, max(0, round(random.gauss(7 + bias * 2, 2))))
            rows.append((survey_id, cid, survey_date.strftime("%Y-%m-%d"), satisfaction, nps))
            survey_id += 1

    conn.executemany(
        """INSERT INTO surveys (survey_id, customer_id, survey_date, satisfaction_score, nps_score)
           VALUES (?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()


def seed_renewals(conn, customers):
    rows = []
    renewal_id = 1
    for cid, _, _, _, signup_date in customers:
        start = datetime.strptime(signup_date, "%Y-%m-%d")
        # simulate 1-2 renewal cycles per customer
        cycles = random.randint(1, 2)
        contract_start = start
        for _ in range(cycles):
            contract_end = contract_start + timedelta(days=365)
            if contract_end > END_DATE:
                contract_end = END_DATE
            renewed = 1 if random.random() < 0.78 else 0
            rows.append(
                (
                    renewal_id,
                    cid,
                    contract_start.strftime("%Y-%m-%d"),
                    contract_end.strftime("%Y-%m-%d"),
                    renewed,
                )
            )
            renewal_id += 1
            if renewed == 0:
                break
            contract_start = contract_end

    conn.executemany(
        """INSERT INTO renewals (renewal_id, customer_id, contract_start, contract_end, renewed)
           VALUES (?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()


def seed_usage(conn, customers):
    rows = []
    usage_id = 1
    for cid, *_ in customers:
        num_logs = random.randint(10, 60)
        for _ in range(num_logs):
            usage_date = random_date()
            feature = random.choice(FEATURES)
            usage_count = random.randint(1, 50)
            rows.append((usage_id, cid, usage_date.strftime("%Y-%m-%d"), feature, usage_count))
            usage_id += 1

    conn.executemany(
        """INSERT INTO usage_logs (usage_id, customer_id, usage_date, feature, usage_count)
           VALUES (?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a synthetic Customer Success SQLite database."
    )
    parser.add_argument(
        "--customers",
        type=int,
        default=DEFAULT_NUM_CUSTOMERS,
        help=f"Number of customers to simulate (default: {DEFAULT_NUM_CUSTOMERS})",
    )
    args = parser.parse_args()

    if args.customers < 1:
        parser.error("--customers must be a positive integer")

    return args


def main():
    args = parse_args()

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    build_schema(conn)

    customers = seed_customers(conn, args.customers)
    seed_tickets(conn, customers)
    seed_surveys(conn, customers)
    seed_renewals(conn, customers)
    seed_usage(conn, customers)

    conn.close()
    print(f"Database created at: {DB_PATH}")
    print(f"Customers simulated: {args.customers}")


if __name__ == "__main__":
    main()
