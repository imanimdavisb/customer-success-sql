"""
main.py
--------
Entry point for the Customer Success SQL project.

Usage:
    python data/generate_data.py   # run once, creates the database
    python src/main.py             # prints KPI report + generates charts
"""

from kpis import print_kpi_report
from charts import generate_all_charts


def main():
    print_kpi_report()
    generate_all_charts()


if __name__ == "__main__":
    main()
