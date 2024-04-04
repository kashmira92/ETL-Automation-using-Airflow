# ETL Automation in the Retail Domain using Apache Airflow
Apache Airflow Project using BigQuery, DBT and Docker.

In this project, an Airflow DAG was orchestrated to efficiently manage the ingestion of raw retail data, into a star schema model within BigQuery. The entire workflow was encapsulated within Docker containers to ensure consistency and portability across environments. The integration of Airflow within Docker was facilitated using the Astro CLI, enabling effective task and dependency management.

The DAG was structured to handle various data operations, starting from the ingestion of raw retail data and culminating in its transformation into a star schema model within BigQuery. Throughout this process, data quality checks were enforced at each step to maintain the integrity and reliability of the data.

To optimize querying and analysis, reporting models were built using DBT on Airflow. These models were constructed on top of the fact and dimension tables, providing a structured and optimized layer for business intelligence tools to utilize.

Furthermore, the DAG was Dockerized and scheduled to seamlessly manage end-to-end data tasks. By incorporating Continuous Integration/Continuous Deployment (CI/CD) processes, the data pipeline remained robust and reliable, capable of efficiently handling large-scale data operations.

## Dataset:
Column:
InvoiceNo -- Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.
StockCode -- Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.
Description -- Product (item) name. Nominal.
Quantity -- The quantities of each product (item) per transaction. Numeric.
InvoiceDate -- Invice Date and time. Numeric, the day and time when each transaction was generated.
UnitPrice -- Unit price. Numeric, Product price per unit in sterling.
CustomerID -- Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.
Country -- Country name. Nominal, the name of the country where each customer resides.
