# Databricks notebook source
# MAGIC %md
# MAGIC Patients data is obtained from database . this is our parent database for patients. We obtained from database and stoired in bronze layer as parquet file which acts as raw data from db source. Now we will clean data , enrich data , implement common data model by implementing  a surrogate key, incorporate SCD2 to keep track of chnages and store as delta table  in silver layer. thsi delta table si present in databricks where ACID are allowed, updates are allowed.

# COMMAND ----------

df_hosa=spark.read.parquet("/mnt/bronze/hosa/patients")
df_hosa.createOrReplaceTempView("patients_hosa")

#Reading Hospital B patient data 
df_hosb=spark.read.parquet("/mnt/bronze/hosb/patients")
df_hosb.createOrReplaceTempView("patients_hosb")

# COMMAND ----------

display(df_hosa)

# COMMAND ----------

display(df_hosb)

# COMMAND ----------

# MAGIC %sql
# MAGIC   CREATE OR REPLACE TEMP VIEW cdm_patients AS
# MAGIC   SELECT CONCAT(SRC_PatientID,'-', datasource) AS Patient_Key, *  --SURROGATE KEY FOR COMMON DATA MODEL
# MAGIC   FROM (
# MAGIC       SELECT 
# MAGIC       PatientID AS SRC_PatientID ,
# MAGIC       FirstName,
# MAGIC       LastName,
# MAGIC       MiddleName,
# MAGIC       SSN,
# MAGIC       PhoneNumber,
# MAGIC       Gender,
# MAGIC       DOB,
# MAGIC       Address,
# MAGIC       ModifiedDate,
# MAGIC       datasource
# MAGIC       FROM patients_hosa
# MAGIC       UNION ALL
# MAGIC       SELECT 
# MAGIC       ID AS SRC_PatientID,
# MAGIC       F_Name AS FirstName,
# MAGIC       L_Name AS LastName,
# MAGIC       M_Name ASMiddleName,
# MAGIC       SSN,
# MAGIC       PhoneNumber,
# MAGIC       Gender,
# MAGIC       DOB,
# MAGIC       Address,
# MAGIC       Updated_Date AS ModifiedDate,
# MAGIC       datasource
# MAGIC        FROM patients_hosb
# MAGIC   )

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from cdm_patients

# COMMAND ----------

# MAGIC   %sql
# MAGIC   CREATE OR REPLACE TEMP VIEW quality_checks AS
# MAGIC   SELECT 
# MAGIC       Patient_Key,
# MAGIC       SRC_PatientID,
# MAGIC       FirstName,
# MAGIC       LastName,
# MAGIC       MiddleName,
# MAGIC       SSN,
# MAGIC       PhoneNumber,
# MAGIC       Gender,
# MAGIC       DOB,
# MAGIC       Address,
# MAGIC       ModifiedDate As SRC_ModifiedDate,
# MAGIC       datasource,
# MAGIC       CASE 
# MAGIC           WHEN SRC_PatientID IS NULL OR dob IS NULL OR firstname IS NULL or lower(firstname)='null' THEN TRUE
# MAGIC           ELSE FALSE
# MAGIC       END AS is_quarantined
# MAGIC   FROM cdm_patients

# COMMAND ----------

# MAGIC %md
# MAGIC ### invalid records - we need to eliminate them

# COMMAND ----------

# MAGIC
# MAGIC %sql
# MAGIC select * from quality_checks where is_quarantined = TRUE

# COMMAND ----------

# MAGIC   %sql
# MAGIC   CREATE OR REPLACE TEMP VIEW quality_checks1 AS
# MAGIC   selEct * from quality_checks where is_quarantined= FALSE

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from quality_checks1 where is_quarantined = TRUE

# COMMAND ----------

# MAGIC   %sql
# MAGIC   CREATE TABLE IF NOT EXISTS silver.patients (
# MAGIC       Patient_Key STRING primary key,
# MAGIC       SRC_PatientID STRING,
# MAGIC       FirstName STRING,
# MAGIC       LastName STRING,
# MAGIC       MiddleName STRING,
# MAGIC       SSN STRING,
# MAGIC       PhoneNumber STRING,
# MAGIC       Gender STRING,
# MAGIC       DOB DATE,
# MAGIC       Address STRING,
# MAGIC       SRC_ModifiedDate TIMESTAMP,
# MAGIC       datasource STRING,
# MAGIC       is_quarantined BOOLEAN,
# MAGIC       inserted_date TIMESTAMP,
# MAGIC       modified_date TIMESTAMP,
# MAGIC       is_current BOOLEAN
# MAGIC   )
# MAGIC   USING DELTA;

# COMMAND ----------

# MAGIC   %sql
# MAGIC   -- Step 1: Mark existing records as historical (is_current = false) for patients that will be updated
# MAGIC   MERGE INTO silver.patients AS target
# MAGIC   USING quality_checks1 AS source
# MAGIC   ON target.Patient_Key = source.Patient_Key
# MAGIC   AND target.is_current = true 
# MAGIC   WHEN MATCHED
# MAGIC   AND (
# MAGIC       target.SRC_PatientID <> source.SRC_PatientID OR
# MAGIC       target.FirstName <> source.FirstName OR
# MAGIC       target.LastName <> source.LastName OR
# MAGIC       target.MiddleName <> source.MiddleName OR
# MAGIC       target.SSN <> source.SSN OR
# MAGIC       target.PhoneNumber <> source.PhoneNumber OR
# MAGIC       target.Gender <> source.Gender OR
# MAGIC       target.DOB <> source.DOB OR
# MAGIC       target.Address <> source.Address OR
# MAGIC       target.SRC_ModifiedDate <> source.SRC_ModifiedDate OR
# MAGIC       target.datasource <> source.datasource OR
# MAGIC       target.is_quarantined <> source.is_quarantined
# MAGIC   )
# MAGIC   THEN UPDATE SET
# MAGIC       target.is_current = false,
# MAGIC       target.modified_date = current_timestamp()
# MAGIC  
# MAGIC  
# MAGIC   WHEN NOT MATCHED
# MAGIC   THEN INSERT (
# MAGIC       Patient_Key,
# MAGIC       SRC_PatientID,
# MAGIC       FirstName,
# MAGIC       LastName,
# MAGIC       MiddleName,
# MAGIC       SSN,
# MAGIC       PhoneNumber,
# MAGIC       Gender,
# MAGIC       DOB,
# MAGIC       Address,
# MAGIC       SRC_ModifiedDate,
# MAGIC       datasource,
# MAGIC       is_quarantined,
# MAGIC       inserted_date,
# MAGIC       modified_date,
# MAGIC       is_current
# MAGIC   )
# MAGIC   VALUES (
# MAGIC       source.Patient_Key,
# MAGIC       source.SRC_PatientID,
# MAGIC       source.FirstName,
# MAGIC       source.LastName,
# MAGIC       source.MiddleName,
# MAGIC       source.SSN,
# MAGIC       source.PhoneNumber,
# MAGIC       source.Gender,
# MAGIC       source.DOB,
# MAGIC       source.Address,
# MAGIC       source.SRC_ModifiedDate,
# MAGIC       source.datasource,
# MAGIC       source.is_quarantined,
# MAGIC       current_timestamp(), -- Set inserted_date to current timestamp
# MAGIC       current_timestamp(), -- Set modified_date to current timestamp
# MAGIC       true -- Mark as current
# MAGIC   );
# MAGIC  

# COMMAND ----------

# MAGIC %md
# MAGIC Now silver.patients is delta table present in silver layer for patients

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from silver.patients
