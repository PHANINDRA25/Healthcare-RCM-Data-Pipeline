# Databricks notebook source
# MAGIC   %sql
# MAGIC   CREATE TABLE IF NOT EXISTS gold.dim_provider
# MAGIC   (
# MAGIC   ProviderID string PRIMARY KEY,
# MAGIC   FirstName string,
# MAGIC   LastName string,
# MAGIC   deptid string,
# MAGIC   NPI long,
# MAGIC   datasource string
# MAGIC   --foreign key (deptid) references gold.dim_department(Dept_Id)
# MAGIC   )

# COMMAND ----------

# MAGIC %sql 
# MAGIC truncate TABLE gold.dim_provider 

# COMMAND ----------

# MAGIC
# MAGIC   %sql
# MAGIC   insert into gold.dim_provider
# MAGIC   select 
# MAGIC   ProviderID ,
# MAGIC   FirstName ,
# MAGIC   LastName ,
# MAGIC   concat(DeptID,'-',datasource) deptid,
# MAGIC   NPI ,
# MAGIC   datasource 
# MAGIC    from silver.providers
# MAGIC    where is_quarantined=false

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from gold.dim_provider
