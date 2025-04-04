# cleaner_consumer.py
from kafka import KafkaConsumer, KafkaProducer
import json
import re
from datetime import datetime

consumer = KafkaConsumer(
    'raw-news',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='news-cleaner',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)  # remove HTML
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    return text.strip()

print("Cleaner started...")
for msg in consumer:
    raw = msg.value
    cleaned = {
        "title": clean_text(raw['title']),
        "summary": clean_text(raw['summary']),
        "link": raw['link'],
        "published": datetime.strptime(raw['published'], '%a, %d %b %Y %H:%M:%S %z').isoformat()
    }
    producer.send('cleaned-news', value=cleaned)
    print(f"Forwarded: {cleaned['title']}")
