-- ASML Genie Code demo: setup and reset
-- Source data: samples.wanderbricks (read-only, on every workspace). No data generation needed.

-- ===== SETUP (run once) =====
CREATE SCHEMA IF NOT EXISTS genie_code_workshop.asml_dry_run COMMENT 'ASML Genie Code hackathon dry run. ';

-- Sanity checks used in the talk track
SELECT COUNT(*) AS reviews, SUM(CASE WHEN is_deleted THEN 1 ELSE 0 END) AS soft_deleted_reviews
FROM samples.wanderbricks.reviews;

SELECT status, COUNT(*) AS bookings FROM samples.wanderbricks.bookings GROUP BY status ORDER BY bookings DESC;

-- ===== RESET (between rehearsals) =====
-- Drops everything Genie Code created in the demo schema, then recreates the empty schema.
-- Also delete demo jobs in the Jobs UI (tag project:asml_demo).
-- DROP SCHEMA IF EXISTS genie_code_workshop.asml_demo CASCADE;
-- CREATE SCHEMA genie_code_workshop.asml_demo
--   COMMENT 'ASML Genie Code hackathon demo output (30 Nov 2026). Safe to drop.';
