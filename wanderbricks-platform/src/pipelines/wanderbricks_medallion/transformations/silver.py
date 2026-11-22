"""Silver layer: cleaned, conformed WanderBricks entities with data quality expectations."""
from pyspark import pipelines as dp
from pyspark.sql import functions as F

SILVER = spark.conf.get("silver_schema")


@dp.materialized_view(
    name=f"{SILVER}.bookings",
    comment="One row per booking. Adds stay length (nights). Status: pending, confirmed, completed, cancelled.",
    table_properties={"quality": "silver"},
)
@dp.expect_all_or_drop({
    "valid_booking_id": "booking_id IS NOT NULL",
    "valid_stay_dates": "check_out > check_in",
})
@dp.expect("non_negative_amount", "total_amount >= 0")
def silver_bookings():
    return (
        spark.read.table("bookings")
        .select(
            "booking_id", "user_id", "property_id", "check_in", "check_out",
            "guests_count", F.col("total_amount").cast("decimal(12,2)").alias("total_amount"),
            F.lower("status").alias("status"), "created_at", "updated_at",
        )
        .withColumn("nights_count", F.datediff("check_out", "check_in"))
    )


@dp.materialized_view(
    name=f"{SILVER}.properties",
    comment="One row per property, enriched with destination and country attributes.",
    table_properties={"quality": "silver"},
)
@dp.expect_or_drop("valid_property_id", "property_id IS NOT NULL")
def silver_properties():
    destinations = spark.read.table("destinations").select(
        "destination_id", "destination", "country", "state_or_province"
    )
    return (
        spark.read.table("properties")
        .drop("_source_table")
        .join(destinations, "destination_id", "left")
    )


@dp.materialized_view(
    name=f"{SILVER}.reviews",
    comment="Active (non-deleted) guest reviews with rating 1-5.",
    table_properties={"quality": "silver"},
)
@dp.expect_or_drop("valid_rating", "rating BETWEEN 1 AND 5")
def silver_reviews():
    return (
        spark.read.table("reviews")
        .filter(~F.coalesce(F.col("is_deleted"), F.lit(False)))
        .select("review_id", "booking_id", "property_id", "user_id", "rating", "comment", "created_at")
    )


@dp.materialized_view(
    name=f"{SILVER}.support_messages",
    comment="Customer support conversations flattened to one row per message (from nested messages array).",
    table_properties={"quality": "silver"},
)
@dp.expect_or_drop("valid_ticket_id", "ticket_id IS NOT NULL")
def silver_support_messages():
    return (
        spark.read.table("customer_support_logs")
        .select(
            "ticket_id", "user_id", "support_agent_id",
            F.to_timestamp("created_at").alias("ticket_created_at"),
            F.posexplode("messages").alias("message_seq", "m"),
        )
        .select(
            "ticket_id", "user_id", "support_agent_id", "ticket_created_at", "message_seq",
            F.col("m.sender").alias("sender"),
            F.col("m.message").alias("message"),
            F.col("m.sentiment").alias("sentiment"),
            F.to_timestamp("m.timestamp").alias("message_sent_at"),
        )
    )
