🛠️ ETL Pipeline with MySQL, Apache Kafka, and Airflow
📌 Overview
This project demonstrates a real-time ETL (Extract, Transform, Load) pipeline using:

~MySQL for source data
~Apache Kafka for streaming messages
~Apache Airflow for scheduling the pipeline
~Python for processing
~dotenv + Fernet for secure credential management

etl_project/
│
├── producer_consumer_etl.py      # Main ETL logic: extract, transform, write, and publish
├── airflow_dag.py                # Airflow DAG to schedule ETL
├── .env                          # Environment variables (not committed)
├── wrapper_script.sh             # Script triggered by Airflow to run the ETL
├── extract/                      # Output directory for CSV files
└── requirements.txt              # Python dependencies


🔁 ETL Workflow
1. Extract: Connects to a MySQL database, decrypts password, and fetches data from customer_data table.
2. Transform: Filters records with age < 30.
3. Load:
   ~ Saves transformed data as CSV in local extract/ folder.
   ~ Publishes records to a Kafka topic.
4. Consume: Kafka consumer listens and prints the streamed messages.
5. Schedule: Airflow runs the ETL every 5 minutes via a Bash script.

📦 Requirements
Install dependencies:
pip install -r requirements.txt

🔒 Password Decryption
Ensure you implement a secure decrypt_password() function using cryptography.fernet. Store keys securely.

🛠️ Airflow DAG
Setup
1. Place airflow_dag.py in Airflow's dags/ directory.
2. Ensure wrapper_script.sh runs the ETL script:

#!/bin/bash
python /home/vishal/etl_project/producer_consumer_etl.py

DAG Details
DAG ID: mysql_etl_dag
Runs every 5 minutes
Task: Executes the ETL using a BashOperator

📌 Notes
~ Use .env and Fernet key securely, do not hardcode credentials.
~ Use Docker or VM for Kafka if not running locally.
~ This pipeline can be extended to push to a data lake (like S3 or HDFS) or warehouse.