# Microsoft Fabric notebook: Bronze -> Silver
# Attach a Lakehouse before execution. Place source CSV at Files/raw/ in OneLake.
from pyspark.sql import functions as F
from pyspark.sql.types import *

source_path = "Files/raw/foia-7a-fy2010-fy2019-asof-250930.csv"
bronze_table = "sba_7a_bronze"
silver_table = "sba_7a_silver"

raw = (spark.read.option("header", True).option("inferSchema", True).csv(source_path))
# Keep source data as landed in Bronze; protect raw PII with workspace permissions.
raw.write.format("delta").mode("overwrite").saveAsTable(bronze_table)

silver = raw.dropDuplicates()
silver = silver.withColumn("ApprovalFY", F.col("ApprovalFY").cast("int"))
silver = silver.withColumn("GrossApproval", F.col("GrossApproval").cast("double"))
silver = silver.withColumn("SBAGuaranteedApproval", F.col("SBAGuaranteedApproval").cast("double"))
silver = silver.withColumn("InitialInterestRate", F.col("InitialInterestRate").cast("double"))
silver = silver.withColumn("TerminMonths", F.col("TerminMonths").cast("int"))
silver = silver.withColumn("JobsSupported", F.col("JobsSupported").cast("double"))
silver = silver.withColumn("BusinessAge", F.col("BusinessAge").cast("double"))
silver = silver.withColumn("ApprovalDateParsed", F.to_date("ApprovalDate", "MM-dd-yyyy"))
silver = silver.withColumn("ApprovalYear", F.year("ApprovalDateParsed"))
silver = silver.withColumn("ApprovalMonth", F.month("ApprovalDateParsed"))
silver = silver.withColumn("target_default",
    F.when(F.col("LoanStatus") == "CHGOFF", 1)
     .when(F.col("LoanStatus") == "PIF", 0)
     .otherwise(F.lit(None)).cast("int"))
silver.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable(silver_table)
print("Bronze rows:", raw.count(), "Silver rows:", silver.count())
display(silver.groupBy("ApprovalFY","LoanStatus").count().orderBy("ApprovalFY","LoanStatus"))
