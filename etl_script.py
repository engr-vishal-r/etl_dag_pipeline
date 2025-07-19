import pymysql
import pandas as pd
from datetime import datetime
from confluent_kafka import Producer
import os
from password_utils import decrypt_password
from dotenv import load_dotenv
import os

load_dotenv()
p = Producer({'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS")})

def delivery_report(err, msg):
    if err is not None:
        print('Delivery failed:', err)
    else:
        print('Message delivered to', msg.topic(), msg.partition())

def fetch_data_from_mysql():
    encrypted_password = os.getenv("ENCRYPTED_PASSWORD")
    decrypted = decrypt_password(encrypted_password.encode())
    mysql_config = {
        'host': os.getenv("HOST"),
        'port': int(os.getenv("PORT")),
        'user': os.getenv("USER"),
        'password': decrypted,
        'database': os.getenv("DATABASE")
    }

    connection = pymysql.connect(**mysql_config)
    query = 'SELECT * FROM customer_data'
    df = pd.read_sql(query, connection)
    print('Connected to database successfully!!')
    connection.close()
    return df

def transform_data(df):
    df_transformed = df[df['age'] < 30]
    print('Data successfully fetched from Database!!')
    return df_transformed

def write_data_to_file(df):
    output_dir = 'F:/E2E_Projects/etl/extract'
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'etl_output_{timestamp}.csv'
    file_path = os.path.join(output_dir, file_name)
    df.to_csv(file_path, index=False)
    print(f'Data written to {file_path}')

def send_to_kafka(df):
    for _, row in df.iterrows():
        message = row.to_json()
        p.produce(os.getenv("KAFKA_TOPIC"), key=str(row['id']), value=message, callback=delivery_report)
    print(f'Messages published successfully to {os.getenv("KAFKA_TOPIC")} !!')
    p.flush()

def etl_process():
    df = fetch_data_from_mysql()
    df_transformed = transform_data(df)
    write_data_to_file(df_transformed)
    send_to_kafka(df_transformed)

if __name__ == "__main__":
    etl_process()