# Healthcare-RCM-Data-Pipeline
An end to end pipeline that ingests EMR, Claims and different health codes data and undergoes cleaning, refining and complex transformations to generate usable data for other business stakeholders. 


An end-to-end data pipeline has been developed to streamline healthcare revenue cycle management (RCM). To start with , a configuration file is used to make the pipeline understand what files it needs to process.  This metadata-driven pipeline is built using Azure Data Factory, ingesting data from diverse sources including SQL databases, flat files, and APIs. It followsMedallion architecture, starting with raw data collection in the bronze layer and utilizing Azure Data Lake Storage Gen2 (ADLS Gen2) for data storage . 

The data is processed using Databricks and PySpark, which help improve quality and organize it into Delta tables across the silver and gold layers. In the gold layer, data is structured into fact and dimension tables to support both full and incremental loads, with consistent logging for auditing.

Further, Microsoft Synapse Analytics processes the data in the gold layer, enabling the creation of insightful Power BI dashboards for end-users. The entire infrastructure is secured and governed by Azure Key Vault and Azure Enterprise ID, ensuring data integrity and compliance.







![Workflow](https://github.com/user-attachments/assets/31f4a647-1302-4c57-9fc0-d1fe9709fa50)
