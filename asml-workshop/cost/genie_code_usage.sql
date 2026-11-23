-- Genie Code usage and cost (segment 4). Based on the queries in
-- https://learn.microsoft.com/en-us/azure/databricks/genie/monitor-cost/
-- Needs SELECT on system.billing. The usage table updates every few hours.

-- 1. Billed Genie Code usage per user per day (last 30 days), at list price
SELECT
  u.usage_date,
  u.identity_metadata.run_as AS run_as_user,
  u.usage_metadata.genie.surface AS genie_surface,
  u.sku_name,
  ROUND(SUM(u.usage_quantity), 2) AS dbus,
  ROUND(SUM(u.usage_quantity * lp.pricing.effective_list.default), 2) AS list_cost
FROM system.billing.usage u
JOIN system.billing.list_prices lp
  ON u.sku_name = lp.sku_name
 AND u.usage_end_time >= lp.price_start_time
 AND (lp.price_end_time IS NULL OR u.usage_end_time < lp.price_end_time)
WHERE u.billing_origin_product = 'GENIE'
  AND u.usage_metadata.genie.surface IN ('GENIE_CODE', 'GENIE_CODE_CLI')
  AND u.sku_name != 'GENIE_FREE_USAGE'
  AND u.usage_date >= DATE_SUB(CURRENT_DATE(), 30)
GROUP BY ALL
ORDER BY u.usage_date DESC, list_cost DESC;

-- 2. Free vs paid DBUs per user, month to date
SELECT
  u.identity_metadata.run_as AS user,
  u.usage_metadata.genie.surface AS genie_surface,
  ROUND(SUM(CASE WHEN u.sku_name = 'GENIE_FREE_USAGE' THEN u.usage_quantity ELSE 0 END), 2) AS free_dbus,
  ROUND(SUM(CASE WHEN u.sku_name != 'GENIE_FREE_USAGE' THEN u.usage_quantity ELSE 0 END), 2) AS paid_dbus
FROM system.billing.usage u
WHERE u.billing_origin_product = 'GENIE'
  AND u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE())
GROUP BY ALL
ORDER BY paid_dbus DESC;
