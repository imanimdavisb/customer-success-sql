"""
charts.py
----------
Generates the four Customer Success charts and saves them as PNGs
in the output/charts/ directory:
  - Satisfaction Trend (line chart)
  - Complaints (stacked bar chart by category over time)
  - Product Usage (line chart by feature)
  - Response Time (line chart, avg first-response hours per month)
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from db import run_query

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output" / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")


def satisfaction_trend():
    query = """
        SELECT strftime('%Y-%m', survey_date) AS month,
               ROUND(AVG(satisfaction_score), 2) AS avg_csat
        FROM surveys
        GROUP BY month
        ORDER BY month;
    """
    df = run_query(query)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["month"], df["avg_csat"], marker="o", color="#2b8a3e")
    ax.set_title("Satisfaction Trend (Avg CSAT by Month)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Avg CSAT (1-5)")
    ax.set_ylim(1, 5)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "satisfaction_trend.png", dpi=150)
    plt.close(fig)


def complaints_chart():
    query = """
        SELECT strftime('%Y-%m', created_at) AS month, category, COUNT(*) AS ticket_count
        FROM tickets
        GROUP BY month, category
        ORDER BY month;
    """
    df = run_query(query)
    pivot = df.pivot(index="month", columns="category", values="ticket_count").fillna(0)

    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    ax.set_title("Support Tickets by Category (Monthly)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Ticket Count")
    ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "complaints.png", dpi=150)
    plt.close(fig)


def product_usage_chart():
    query = """
        SELECT strftime('%Y-%m', usage_date) AS month, feature, SUM(usage_count) AS total_usage
        FROM usage_logs
        GROUP BY month, feature
        ORDER BY month;
    """
    df = run_query(query)
    pivot = df.pivot(index="month", columns="feature", values="total_usage").fillna(0)

    fig, ax = plt.subplots(figsize=(10, 5))
    for feature in pivot.columns:
        ax.plot(pivot.index, pivot[feature], marker="o", label=feature)
    ax.set_title("Product Usage by Feature (Monthly)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Usage Count")
    ax.legend(title="Feature", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "product_usage.png", dpi=150)
    plt.close(fig)


def response_time_chart():
    query = """
        SELECT strftime('%Y-%m', created_at) AS month,
               ROUND(AVG((julianday(first_response_at) - julianday(created_at)) * 24), 2) AS avg_response_hours
        FROM tickets
        GROUP BY month
        ORDER BY month;
    """
    df = run_query(query)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["month"], df["avg_response_hours"], marker="o", color="#e8590c")
    ax.set_title("Avg First-Response Time (Hours) by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Avg Response Time (hrs)")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "response_time.png", dpi=150)
    plt.close(fig)


def generate_all_charts():
    satisfaction_trend()
    complaints_chart()
    product_usage_chart()
    response_time_chart()
    print(f"Charts saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all_charts()
