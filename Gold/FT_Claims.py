# Databricks notebook source
# MAGIC   %sql
# MAGIC   CREATE TABLE IF NOT EXISTS gold.dim_claims (
# MAGIC   ClaimID string primary key,
# MAGIC   SRC_ClaimID string,
# MAGIC   FK_TransactionID string,
# MAGIC   FK_Patient_ID string,
# MAGIC   FK_EncounterID string,
# MAGIC   FK_Provider_ID string,
# MAGIC   FK_DeptID string,
# MAGIC   ServiceDate date,
# MAGIC   ClaimDate date,
# MAGIC   PayorID string,
# MAGIC   ClaimAmount string,
# MAGIC   PaidAmount string,
# MAGIC   ClaimStatus string,
# MAGIC   PayorType string,
# MAGIC   Deductible string,
# MAGIC   Coinsurance string,
# MAGIC   Copay string,
# MAGIC   SRC_InsertDate date,
# MAGIC   SRC_ModifiedDate date,
# MAGIC   datasource string,
# MAGIC   is_quarantined boolean,
# MAGIC   audit_insertdate timestamp,
# MAGIC   audit_modifieddate timestamp,
# MAGIC   is_current boolean
# MAGIC   --   constraint fk_encounter1 foreign key (FK_EncounterID) references gold.dim_encounters(EncounterID),
# MAGIC   -- constraint fk_patient1 foreign key (FK_Patient_ID) references gold.dim_patient(patient_key),
# MAGIC   -- constraint fk_provider1 foreign key (FK_Provider_ID) references gold.dim_provider(ProviderID),
# MAGIC   -- constraint fk_dept1 foreign key (FK_DeptID) references gold.dim_department(Dept_Id),
# MAGIC   -- constraint fk_transaction1 foreign key (FK_TransactionID) references gold.fact_transactions(TransactionID)
# MAGIC   )

# COMMAND ----------

# MAGIC %sql 
# MAGIC truncate TABLE gold.dim_claims

# COMMAND ----------

# MAGIC   %sql
# MAGIC   insert into gold.dim_claims
# MAGIC   select
# MAGIC         ClaimID,
# MAGIC       SRC_ClaimID,
# MAGIC      
# MAGIC       concat(PatientID,'-',datasource ) as FK_TransactionID,
# MAGIC       concat(PatientID,'-',datasource ) as FK_Patient_ID,
# MAGIC       concat(EncounterID,'-',datasource) as FK_EncounterID,
# MAGIC       case when datasource='hos-a' then concat('H1-',providerID) else concat('H2-',providerID ) end as FK_Provider_ID,
# MAGIC       concat(DeptID,'-',datasource ) as FK_DeptID,
# MAGIC       ServiceDate,
# MAGIC       ClaimDate,
# MAGIC       PayorID,
# MAGIC       ClaimAmount,
# MAGIC       PaidAmount,
# MAGIC       ClaimStatus,
# MAGIC       PayorType,
# MAGIC       Deductible,
# MAGIC       Coinsurance,
# MAGIC       Copay,
# MAGIC       SRC_InsertDate,
# MAGIC       SRC_ModifiedDate,
# MAGIC       datasource,
# MAGIC       is_quarantined,
# MAGIC       audit_insertdate,
# MAGIC       audit_modifieddate,
# MAGIC       is_current
# MAGIC       from silver.claims 
# MAGIC       where is_current=true and is_quarantined=false

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from gold.dim_claims

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table  silver.claims
# MAGIC
# MAGIC --drop table  from gold.dim_claims

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table   silver.cptcodes
# MAGIC drop table   silver.icd_codes
# MAGIC drop table   silver.npi_extract
# MAGIC drop table   gold.dim_cpt_code
# MAGIC drop table   gold.dim_icd
# MAGIC drop table   gold.dim_npi
