"""
kpis.py
--------
Computes the four top-level Customer Success KPIs:
  - Customer Satisfaction (CSAT)
  - Net Promoter Score (NPS)
  - Renewal Rate
  - Tickets Closed

Each KPI is computed via a SQL query executed against customer_success.db.
"""

from db import run_query

CSAT_QUERY = """
SELECT ROUND(AVG(satisfaction_score), 2) AS avg_csat
FROM surveys;
"""

NPS_QUERY = """
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) / COUNT(*)
        - 100.0 * SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) / COUNT(*)
    , 1) AS nps_score
FROM surveys;
"""

RENEWAL_RATE_QUERY = """
SELECT
    ROUND(100.0 * SUM(renewed) / COUNT(*), 1) AS renewal_rate_pct
FROM renewals;
"""

TICKETS_CLOSED_QUERY = """
SELECT COUNT(*) AS tickets_closed
FROM tickets
WHERE status = 'Closed';
"""


def get_kpis() -> dict:
    """Return a dict with all four KPI values."""
    csat = run_query(CSAT_QUERY).iloc[0, 0]
    nps = run_query(NPS_QUERY).iloc[0, 0]
    renewal_rate = run_query(RENEWAL_RATE_QUERY).iloc[0, 0]
    tickets_closed = int(run_query(TICKETS_CLOSED_QUERY).iloc[0, 0])

    return {
        "Customer Satisfaction (CSAT)": f"{csat} / 5",
        "Net Promoter Score (NPS)": f"{nps}",
        "Renewal Rate": f"{renewal_rate}%",
        "Tickets Closed": f"{tickets_closed}",
    }


def print_kpi_report():
    kpis = get_kpis()
    print("\n=== Customer Success — Top KPIs ===")
    for name, value in kpis.items():
        print(f"{name:.<35} {value}")
    print()


if __name__ == "__main__":
    print_kpi_report()
