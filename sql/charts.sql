-- ==========================================================
-- charts.sql
-- Queries that feed the visualizations in src/charts.py
-- ==========================================================

-- A. Satisfaction Trend — average CSAT per month
SELECT
    strftime('%Y-%m', survey_date) AS month,
    ROUND(AVG(satisfaction_score), 2) AS avg_csat
FROM surveys
GROUP BY month
ORDER BY month;

-- B. Complaints — ticket volume by category over time (complaints highlighted)
SELECT
    strftime('%Y-%m', created_at) AS month,
    category,
    COUNT(*) AS ticket_count
FROM tickets
GROUP BY month, category
ORDER BY month;

-- C. Product Usage — total usage count per feature per month
SELECT
    strftime('%Y-%m', usage_date) AS month,
    feature,
    SUM(usage_count) AS total_usage
FROM usage_logs
GROUP BY month, feature
ORDER BY month;

-- D. Response Time — average first-response time (in hours) per month
SELECT
    strftime('%Y-%m', created_at) AS month,
    ROUND(AVG(
        (julianday(first_response_at) - julianday(created_at)) * 24
    ), 2) AS avg_response_hours
FROM tickets
GROUP BY month
ORDER BY month;
