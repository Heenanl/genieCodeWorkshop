# Project context: WanderBricks booking revenue

> Version-controlled project memory. Change it through merge requests.

## Purpose

Trusted daily booking revenue per destination and property type, so commercial teams can act on destinations whose revenue is dropping. (ASML analogy: output KPI per machine type from production runs.)

## Owners and SLA

| Item | Value |
| --- | --- |
| Owning team | data_services |
| Job | `wanderbricks_booking_revenue_daily` |
| Schedule | Daily 06:00 Europe/Amsterdam |
| Freshness SLA | Gold tables ready by 07:00 Europe/Amsterdam |
| On failure | Email the job owner; two automatic retries, 5 min apart |

## Tables

| Table | Layer | Source | Notes |
| --- | --- | --- | --- |
| `silver_bookings` | silver | `samples.wanderbricks.bookings`, `booking_updates` | Latest status per booking |
| `silver_guests` | silver | `samples.wanderbricks.users` | `email` hashed, `name` dropped |
| `gold_booking_revenue_daily` | gold | `silver_bookings`, `samples.wanderbricks.properties`, `destinations` | One row per day x destination x property type |

## Metric definitions

- **Revenue scope (applies to every metric)**: cancelled bookings (`status = 'cancelled'`) are always excluded. In the sample data that's 15,285 of 72,247 bookings.
- **net_revenue_amount**: sum of `total_amount` for non-cancelled bookings, by `check_in` date.
- **booking_count**: number of non-cancelled bookings, by `check_in` date.
- **avg_booking_value**: `net_revenue_amount / booking_count`.

## Decisions

| Date | Decision | Why |
| --- | --- | --- |
| 2026-11-22 | Jobs, not SDP | Team standard |
| 2026-11-24 | Exclude cancelled bookings from revenue | They never generate revenue |
| 2026-11-24 | Use latest status from `booking_updates` | Bookings change after creation |
| 2026-11-22 | Full overwrite of gold daily | Small data; simpler than MERGE |
| 2026-11-24 | Genie Ontology for structured data access, not Genie Agents | Genie Agents are being phased out |
| 2026-11-24 | Target `uaigw_fe.asml_demo` instead of `genie_code_workshop.asml_demo` | `genie_code_workshop` doesn't exist and we lack CREATE CATALOG; chosen by the user |
| 2026-11-24 | UC tags: `data_classification = pii` on silver only; no `pii` tag | Governed tag policies only allow domain (finance, sales, supply_chain, quality, hr, operations), pii (ssn, address), data_classification (u-nnpi, cui, pii). PII is still labelled via TBLPROPERTIES and comments |

## Known risks

- Currency handling is out of scope for the demo.
