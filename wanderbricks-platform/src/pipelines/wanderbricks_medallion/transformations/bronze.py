"""Bronze layer: 1:1 copies of the WanderBricks source tables.

Metadata-driven: the list of tables comes from the `bronze_tables` pipeline
configuration (see resources/pipelines/wanderbricks_medallion.pipeline.yml).
Adding a table to that list is all that is needed to ingest it.
"""
from pyspark import pipelines as dp
from pyspark.sql import functions as F

SOURCE_CATALOG = spark.conf.get("source_catalog")
SOURCE_SCHEMA = spark.conf.get("source_schema")
BRONZE_TABLES = [t.strip() for t in spark.conf.get("bronze_tables").split(",") if t.strip()]


def define_bronze_table(table_name: str) -> None:
    source = f"{SOURCE_CATALOG}.{SOURCE_SCHEMA}.{table_name}"

    @dp.materialized_view(
        name=table_name,
        comment=f"Bronze copy of {source}. Raw, no business logic applied.",
        table_properties={"quality": "bronze"},
    )
    def _bronze():
        return (
            spark.read.table(source)
            .withColumn("_source_table", F.lit(source))
        )


for _table in BRONZE_TABLES:
    define_bronze_table(_table)
