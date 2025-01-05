-- Databricks notebook source
-- MAGIC %md
-- MAGIC ### Claims & codes

-- COMMAND ----------


drop table  silver.claims

-- COMMAND ----------


drop table   silver.cptcodes

-- COMMAND ----------

drop table   silver.icd_codes

-- COMMAND ----------

drop table   silver.npi_extract

-- COMMAND ----------

drop table   gold.dim_cpt_code

-- COMMAND ----------

drop table   gold.dim_icd

-- COMMAND ----------

drop table   gold.dim_npi

-- COMMAND ----------

drop table   gold.dim_claims

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### EMR

-- COMMAND ----------

drop table silver.departments

-- COMMAND ----------

drop table silver.providers

-- COMMAND ----------

drop table silver.encounters

-- COMMAND ----------

drop table silver.patients

-- COMMAND ----------

drop table silver.transactions

-- COMMAND ----------

drop table gold.dim_department

-- COMMAND ----------

drop table gold.dim_encounters

-- COMMAND ----------

drop table gold.dim_patient

-- COMMAND ----------

drop table gold.dim_provider

-- COMMAND ----------

drop table gold.fact_transactions

-- COMMAND ----------

drop table audit.load_logs

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Silver - select *

-- COMMAND ----------

select * from silver.patients

-- COMMAND ----------

select * from silver.encounters

-- COMMAND ----------

select * from silver.providers

-- COMMAND ----------

select * from silver.departments

-- COMMAND ----------

select * from silver.transactions

-- COMMAND ----------

select * from silver.claims

-- COMMAND ----------

select * from  silver.cptcodes

-- COMMAND ----------

select * from silver.icd_codes

-- COMMAND ----------

select * from silver.npi_extract

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Gold - select *

-- COMMAND ----------

select * from gold.fact_transactions

-- COMMAND ----------

select * from gold.dim_provider

-- COMMAND ----------

select * from gold.dim_patient

-- COMMAND ----------

select * from gold.dim_encounters

-- COMMAND ----------

select * from gold.dim_department

-- COMMAND ----------

select * from gold.dim_cpt_code

-- COMMAND ----------

select * from gold.dim_icd

-- COMMAND ----------

select * from gold.dim_npi

-- COMMAND ----------

select * from gold.dim_claims
