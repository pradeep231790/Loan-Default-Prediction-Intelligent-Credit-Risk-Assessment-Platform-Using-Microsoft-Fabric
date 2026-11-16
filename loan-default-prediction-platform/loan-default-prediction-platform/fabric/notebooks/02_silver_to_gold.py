# Microsoft Fabric notebook: Silver -> Gold curated model and analytics tables
from pyspark.sql import functions as F

silver = spark.table("sba_7a_silver")
gold = (silver
    .filter(F.col("ApprovalFY").between(2014, 2019))
    .filter(F.col("LoanStatus").isin("PIF","CHGOFF"))
    .filter(F.col("ApprovalYear").isNotNull())
    .select(
        "ApprovalFY","ApprovalYear","ApprovalMonth","LoanStatus","target_default",
        "GrossApproval","SBAGuaranteedApproval","InitialInterestRate","TerminMonths",
        "JobsSupported","BusinessAge","ProcessingMethod","Subprogram","BorrState",
        "ProjectState","BusinessType","CollateralInd","FixedorVariableInterestRate",
        "RevolverStatus","NAICSDescription","SBADistrictOffice"
    )
)
gold.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("sba_7a_gold_ml")
display(gold.groupBy("ApprovalFY","target_default").count().orderBy("ApprovalFY","target_default"))
