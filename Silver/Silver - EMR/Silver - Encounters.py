# Databricks notebook source
# Databricks notebook source
from pyspark.sql import SparkSession, functions as f

#Reading Hospital A departments data 
df_hosa=spark.read.parquet("/mnt/bronze/hosa/encounters")

#Reading Hospital B departments data 
df_hosb=spark.read.parquet("/mnt/bronze/hosb/encounters")

#union two departments dataframes
df_merged = df_hosa.unionByName(df_hosb)
display(df_merged)

df_merged.createOrReplaceTempView("encounters")

# COMMAND ----------

# MAGIC   %sql
# MAGIC   CREATE OR REPLACE TEMP VIEW quality_checks AS
# MAGIC   SELECT 
# MAGIC   concat(EncounterID,'-',datasource) as EncounterID,
# MAGIC   EncounterID SRC_EncounterID,
# MAGIC   PatientID,
# MAGIC   EncounterDate,
# MAGIC   EncounterType,
# MAGIC   ProviderID,
# MAGIC   DepartmentID,
# MAGIC   ProcedureCode,
# MAGIC   InsertedDate as SRC_InsertedDate,
# MAGIC   ModifiedDate as SRC_ModifiedDate,
# MAGIC   datasource,
# MAGIC       CASE 
# MAGIC           WHEN EncounterID IS NULL OR PatientID IS NULL THEN TRUE
# MAGIC           ELSE FALSE
# MAGIC       END AS is_quarantined
# MAGIC   FROM encounters

# COMMAND ----------

# MAGIC
# MAGIC %sql
# MAGIC select * from quality_checks where is_quarantined = TRUE

# COMMAND ----------

# MAGIC   %sql
# MAGIC   CREATE OR REPLACE TEMP VIEW quality_checks1 AS
# MAGIC   selEct * from quality_checks where is_quarantined= FALSE

# COMMAND ----------

# MAGIC   %sql
# MAGIC   CREATE TABLE IF NOT EXISTS silver.encounters (
# MAGIC   EncounterID string primary key,
# MAGIC   SRC_EncounterID string,
# MAGIC   PatientID string,
# MAGIC   EncounterDate date,
# MAGIC   EncounterType string,
# MAGIC   ProviderID string,
# MAGIC   DepartmentID string,
# MAGIC   ProcedureCode integer,
# MAGIC   SRC_InsertedDate date,
# MAGIC   SRC_ModifiedDate date,
# MAGIC   datasource string,
# MAGIC   is_quarantined boolean,
# MAGIC   audit_insertdate timestamp,
# MAGIC   audit_modifieddate timestamp,
# MAGIC   is_current boolean
# MAGIC   )
# MAGIC   USING DELTA;

# COMMAND ----------

# MAGIC   %sql
# MAGIC   -- Update old record to implement SCD Type 2
# MAGIC   MERGE INTO silver.encounters AS target
# MAGIC   USING quality_checks1 AS source
# MAGIC   ON target.EncounterID = source.EncounterID AND target.is_current = true
# MAGIC   WHEN MATCHED AND (
# MAGIC       target.SRC_EncounterID != source.SRC_EncounterID OR
# MAGIC       target.PatientID != source.PatientID OR
# MAGIC       target.EncounterDate != source.EncounterDate OR
# MAGIC       target.EncounterType != source.EncounterType OR
# MAGIC       target.ProviderID != source.ProviderID OR
# MAGIC       target.DepartmentID != source.DepartmentID OR
# MAGIC       target.ProcedureCode != source.ProcedureCode OR
# MAGIC       target.SRC_InsertedDate != source.SRC_InsertedDate OR
# MAGIC       target.SRC_ModifiedDate != source.SRC_ModifiedDate OR
# MAGIC       target.datasource != source.datasource OR
# MAGIC       target.is_quarantined != source.is_quarantined
# MAGIC   ) THEN
# MAGIC     UPDATE SET
# MAGIC       target.is_current = false,
# MAGIC       target.audit_modifieddate = current_timestamp()
# MAGIC  

# COMMAND ----------

# MAGIC   %sql
# MAGIC   -- Insert new record to implement SCD Type 2
# MAGIC   MERGE INTO silver.encounters AS target USING quality_checks1 AS source ON target.EncounterID = source.EncounterID
# MAGIC   AND target.is_current = true
# MAGIC   WHEN NOT MATCHED THEN
# MAGIC   INSERT
# MAGIC     (
# MAGIC       EncounterID,
# MAGIC       SRC_EncounterID,
# MAGIC       PatientID,
# MAGIC       EncounterDate,
# MAGIC       EncounterType,
# MAGIC       ProviderID,
# MAGIC       DepartmentID,
# MAGIC       ProcedureCode,
# MAGIC       SRC_InsertedDate,
# MAGIC       SRC_ModifiedDate,
# MAGIC       datasource,
# MAGIC       is_quarantined,
# MAGIC       audit_insertdate,
# MAGIC       audit_modifieddate,
# MAGIC       is_current
# MAGIC     )
# MAGIC   VALUES
# MAGIC     (
# MAGIC       source.EncounterID,
# MAGIC       source.SRC_EncounterID,
# MAGIC       source.PatientID,
# MAGIC       source.EncounterDate,
# MAGIC       source.EncounterType,
# MAGIC       source.ProviderID,
# MAGIC       source.DepartmentID,
# MAGIC       source.ProcedureCode,
# MAGIC       source.SRC_InsertedDate,
# MAGIC       source.SRC_ModifiedDate,
# MAGIC       source.datasource,
# MAGIC       source.is_quarantined,
# MAGIC       current_timestamp(),
# MAGIC       current_timestamp(),
# MAGIC       true
# MAGIC     );
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC
# MAGIC
# MAGIC %sql
# MAGIC select SRC_EncounterID,datasource,count(patientid) from  silver.encounters
# MAGIC group by all
# MAGIC order by 3 desc

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from silver.encounters

# COMMAND ----------


