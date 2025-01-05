# Databricks notebook source
# MAGIC   %sql
# MAGIC   CREATE TABLE IF NOT EXISTS gold.dim_encounters (
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
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC truncate TABLE gold.dim_encounters

# COMMAND ----------

# MAGIC   %sql
# MAGIC   insert into gold.dim_encounters
# MAGIC   select
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
# MAGIC          from silver.encounters
# MAGIC    where is_quarantined=false and is_current=true

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from gold.dim_encounters

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from silver.encounters
