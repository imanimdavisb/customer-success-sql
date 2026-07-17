-- ==========================================================
-- kpis.sql
-- Core Customer Success KPI queries
-- ==========================================================

-- 1. Customer Satisfaction (CSAT) — average satisfaction score (1-5 scale)
SELECT ROUND(AVG(satisfaction_score), 2) AS avg_csat
FROM surveys;

-- 2. Net Promoter Score (NPS)
-- Promoters: score 9-10, Passives: 7-8, Detractors: 0-6
-- NPS = %Promoters - %Detractors
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) / COUNT(*)
        - 100.0 * SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) / COUNT(*)
    , 1) AS nps_score
FROM surveys;

-- 3. Renewal Rate — % of contracts that were renewed
SELECT
    ROUND(100.0 * SUM(renewed) / COUNT(*), 1) AS renewal_rate_pct
FROM renewals;

-- 4. Tickets Closed — total tickets resolved
SELECT COUNT(*) AS tickets_closed
FROM tickets
WHERE status = 'Closed';
