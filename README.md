# Customer Success Analytics — SQL + Python

A portfolio project that simulates a SaaS company's **Customer Success** data
and uses **SQL + Python** to compute key metrics and generate charts,
the kind of dashboard a Customer Success or Ops team might rely on.

## What it does

The project generates a synthetic SQLite database of customers, support
tickets, satisfaction/NPS surveys, contract renewals, and product usage logs,
then runs SQL queries to compute:

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
