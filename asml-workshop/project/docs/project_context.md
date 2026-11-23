# Project context: WanderBricks property health

> Version-controlled project memory. Change it through merge requests.

## Purpose

Daily health score per property from guest reviews and bookings, so operations can act on properties whose guest experience is dropping. (ASML analogy: machine health from sensor readings.)

## Owners and SLA

| Item | Value |
| --- | --- |
| Owning team | data_services |
| Job | `wanderbricks_property_health_daily` |
| Schedule | Daily 06:00 Europe/Amsterdam |
| Freshness SLA | Gold tables ready by 07:00 Europe/Amsterdam |
| On failure | Email the job owner; one automatic retry after 5 min |

## Tables

| Table | Layer | Source | Notes |
| --- | --- | --- | --- |
| `silver_reviews` | silver | `samples.wanderbricks.reviews` | Non-deleted reviews; `comment` is PII (FREEFORM) |
| `silver_guests` | silver | `samples.wanderbricks.users` | `email` hashed, `name` dropped |
| `gold_property_health_daily` | gold | `silver_reviews`, `samples.wanderbricks.bookings` | One row per property per day |

## Metric definitions

- **Review scope (applies to every metric)**: reviews with `is_deleted = true` in `samples.wanderbricks.reviews` are soft-deleted and are always excluded. `review_id` is not unique (1,000 distinct values over 99,793 rows), so count review rows, not distinct `review_id`.
- **avg_rating_30d**: average `rating` of non-deleted reviews created in the last 30 days.
- **rating_trend**: `avg_rating_30d` minus the average rating for the previous 30 days.
- **at_risk**: `rating_trend <= -0.5` AND at least 5 reviews in the last 30 days.
- **booking_count_30d**: bookings with `status IN ('confirmed', 'completed')` and `check_in` in the last 30 days.

## Decisions

| Date | Decision | Why |
| --- | --- | --- |
| 2026-11-22 | Jobs, not SDP | Team standard |
| 2026-11-22 | Exclude `is_deleted` reviews and cancelled bookings | They don't reflect guest experience |
| 2026-11-22 | Full overwrite of gold daily | Small data; simpler than MERGE |
