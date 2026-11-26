-- ASML Genie Code demo: setup and reset
-- Source data: samples.wanderbricks (read-only, on every workspace). No data generation needed.

-- ===== SETUP (run once) =====
CREATE SCHEMA IF NOT EXISTS uaigw_fe.asml_dry_run COMMENT 'ASML Genie Code hackathon dry run. ';
CREATE SCHEMA IF NOT EXISTS uaigw_fe.asml_demo
  COMMENT 'ASML Genie Code hackathon demo output (30 Nov 2026). Safe to drop.';

-- Sanity checks used in the talk track
-- Memory demo (2d): cancelled bookings are excluded from net revenue (15,285 rows, ~8.4M total_amount)
SELECT status, COUNT(*) AS bookings, ROUND(SUM(total_amount)) AS total_amount
FROM samples.wanderbricks.bookings GROUP BY status ORDER BY bookings DESC;

-- ===== RESET (between rehearsals) =====
-- Drops everything Genie Code created in the demo schema, then recreates the empty schema.
-- Also delete demo jobs in the Jobs UI (tag project:asml_demo).
-- DROP SCHEMA IF EXISTS uaigw_fe.asml_demo CASCADE;
-- CREATE SCHEMA uaigw_fe.asml_demo
--   COMMENT 'ASML Genie Code hackathon demo output (30 Nov 2026). Safe to drop.';
