# consumer/logger_consumer.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'cleaned-news',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='news-logger',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Logger started...")
for msg in consumer:
    data = msg.value
    print(f"[{data['published']}] {data['title']}")
