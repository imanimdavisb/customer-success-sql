# Customer Success Analytics — SQL + Python

A portfolio project that simulates a SaaS company's **Customer Success** data
and uses **SQL + Python** to compute key metrics and generate charts,
the kind of dashboard a Customer Success or Ops team might rely on.

![Customer Success Dashboard](output/charts/satisfaction_trend.png)
> **Note:** All data is synthetically generated for demonstration purposes and does not represent any real company, customers, or SaaS product.

## What it does

The project generates a synthetic SQLite database of customers, support
tickets, satisfaction/NPS surveys, contract renewals, and product usage logs,
then runs SQL queries to compute:

## Business Problem

[#business-problem](#business-problem)

Customer Success and Ops teams need fast answers to questions like:

- Is customer satisfaction trending up or down?
- Which complaint categories are driving the most support volume?
- Are we at risk of losing revenue — is the renewal rate slipping?
- Is the team keeping up with tickets, or is response time creeping up?

Instead of pulling these numbers manually from separate systems (support
tickets, survey tools, billing/contracts), this project centralizes them
in one SQL-backed model with a single command to regenerate the full report.

## Key Findings

[#key-findings](#key-findings)

Based on the sample run in this README:

- **CSAT sits at 3.67 / 5** — solidly middling, with room to improve
- **NPS is negative (-14.7)**, meaning detractors currently outnumber promoters —
  a signal worth digging into by complaint category
- **Renewal rate is 75.4%**, meaning roughly 1 in 4 contracts churn — a natural
  next step would be cross-referencing this against CSAT/NPS per account
- **787 tickets closed** in the simulated window, with the "Complaints by Category"
  chart showing where ticket volume concentrates

*(All figures come from the synthetic dataset described below — they
illustrate the kind of insight the queries surface, not a real company's
performance.)*

### Top KPIs
| KPI | Description |
|---|---|
| **Customer Satisfaction (CSAT)** | Average satisfaction score from post-interaction surveys (1–5 scale) |
| **NPS** | Net Promoter Score — % Promoters (9–10) minus % Detractors (0–6) |
| **Renewal Rate** | % of contracts renewed vs. churned |
| **Tickets Closed** | Total number of resolved support tickets |

### Charts
| Chart | Description |
|---|---|
| **Satisfaction Trend** | Average CSAT over time |
| **Complaints** | Support ticket volume by category, month over month |
| **Product Usage** | Feature usage over time |
| **Response Time** | Average first-response time (hours) per month |

## Project structure

- `data/generate_data.py` — builds the synthetic SQLite database
- `sql/kpis.sql` — raw SQL for each top-level KPI
- `sql/charts.sql` — raw SQL feeding each chart
- `src/db.py` — DB connection + query helper
- `src/kpis.py` — computes & prints the KPI report
- `src/charts.py` — generates chart PNGs
- `src/main.py` — runs everything end-to-end
- `output/charts/` — generated PNG charts
- `requirements.txt`
- `README.md`

## Getting started

```bash
# 1. clone and install dependencies
git clone <your-repo-url>
cd customer-success-sql
pip install -r requirements.txt

# 2. generate the synthetic database (run once)
python data/generate_data.py

# optional: control how many customers get simulated (default: 150)
python data/generate_data.py --customers 500

# 3. run the KPI report + generate charts
cd src
python main.py
```

## Sample output

```
=== Customer Success — Top KPIs ===
Customer Satisfaction (CSAT)....... 3.67 / 5
Net Promoter Score (NPS)........... -14.7
Renewal Rate....................... 75.4%
Tickets Closed..................... 787

Charts saved to: output/charts
```

## Example charts

![Complaints by Category](output/charts/complaints.png)
![Product Usage](output/charts/product_usage.png)
![Response Time](output/charts/response_time.png)

## Tech stack

- **Python 3** — data generation, orchestration, visualization
- **SQLite** — lightweight relational database
- **SQL** — all KPI and chart calculations (see `/sql`)
- **pandas** — query results → DataFrames
- **matplotlib** — chart rendering
- **Faker** — realistic synthetic customer names/data

## Notes on the data

All data is synthetically generated (seeded for reproducibility) and does
not represent any real company or customers. Ticket response/resolution
times, satisfaction scores, and renewal outcomes are randomly modeled with
realistic distributions and a small "sentiment bias" per customer so trends
look natural across time.

## Possible extensions

- Swap SQLite for PostgreSQL and connect via `psycopg2`
- Add a filter by `plan` or `industry` to KPIs/charts
- Build a Streamlit or Dash front-end on top of `src/kpis.py` and `src/charts.py`
- Add cohort-based renewal rate (renewal rate by signup month)
