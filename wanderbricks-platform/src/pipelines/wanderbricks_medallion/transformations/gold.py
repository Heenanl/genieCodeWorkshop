"""Gold layer: business-ready aggregates. Metric views are layered on top of these.

Business rules follow docs/reference/wanderbricks-analytics-handbook.md:
  * GBV (1.1)          = SUM(total_amount) WHERE status = 'confirmed', time dimension = created_at
  * Net Revenue (1.2)  = GBV * 0.15 ; Host Payout = GBV * 0.85
  * ADR (1.3)          = SUM(total_amount) / booked nights WHERE status IN ('confirmed','completed')
"""
from pyspark import pipelines as dp
from pyspark.sql import functions as F

SILVER = spark.conf.get("silver_schema")
GOLD = spark.conf.get("gold_schema")

PLATFORM_COMMISSION_RATE = 0.15
GBV_STATUSES = ["confirmed"]
ADR_STATUSES = ["confirmed", "completed"]


def _gbv(col="total_amount"):
    return F.sum(F.when(F.col("status").isin(GBV_STATUSES), F.col(col)))


@dp.materialized_view(
    name=f"{GOLD}.destination_revenue_monthly",
    comment=(
        "Grain: one row per destination per booking-creation month (created_at). "
        "GBV = confirmed bookings only; net revenue = 15% of GBV (handbook 1.1-1.2)."
    ),
    table_properties={"quality": "gold"},
)
def gold_destination_revenue_monthly():
    bookings = spark.read.table(f"{SILVER}.bookings")
    properties = spark.read.table(f"{SILVER}.properties").select("property_id", "destination_id", "destination", "country")
    return (
        bookings.join(properties, "property_id", "inner")
        .withColumn("booking_month", F.trunc("created_at", "month"))
        .groupBy("destination_id", "destination", "country", "booking_month")
        .agg(
            F.count("booking_id").alias("booking_count"),
            F.sum(F.when(F.col("status").isin(GBV_STATUSES), 1).otherwise(0)).alias("confirmed_booking_count"),
            _gbv().alias("gross_booking_value_amount"),
        )
        .withColumn("net_revenue_amount", F.col("gross_booking_value_amount") * F.lit(PLATFORM_COMMISSION_RATE))
        .withColumn("host_payout_amount", F.col("gross_booking_value_amount") * F.lit(1 - PLATFORM_COMMISSION_RATE))
    )


@dp.materialized_view(
    name=f"{GOLD}.property_performance",
    comment="Grain: one row per property. Booking volume, GBV (confirmed), ADR (confirmed+completed) and guest rating.",
    table_properties={"quality": "gold"},
)
def gold_property_performance():
    bookings = (
        spark.read.table(f"{SILVER}.bookings")
        .groupBy("property_id")
        .agg(
            F.count("booking_id").alias("booking_count"),
            F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias("cancelled_booking_count"),
            _gbv().alias("gross_booking_value_amount"),
            F.sum(F.when(F.col("status").isin(ADR_STATUSES), F.col("total_amount"))).alias("adr_revenue_amount"),
            F.sum(F.when(F.col("status").isin(ADR_STATUSES), F.col("nights_count"))).alias("booked_nights_count"),
        )
        .withColumn("average_daily_rate_amount", F.col("adr_revenue_amount") / F.col("booked_nights_count"))
    )
    reviews = (
        spark.read.table(f"{SILVER}.reviews")
        .groupBy("property_id")
        .agg(F.count("review_id").alias("review_count"), F.avg("rating").alias("avg_rating"))
    )
    properties = spark.read.table(f"{SILVER}.properties").select(
        "property_id", "host_id", "title", "property_type", "destination", "country", "base_price"
    )
    return (
        properties.join(bookings, "property_id", "left")
        .join(reviews, "property_id", "left")
    )
