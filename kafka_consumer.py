from confluent_kafka import Consumer
from dotenv import load_dotenv
import os

load_dotenv()
c = Consumer({
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe([os.getenv("KAFKA_TOPIC")])

while True:
    msg = c.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error:", msg.error())
        continue

    print(f"Received message: {msg.value().decode('utf-8')}")

c.close()