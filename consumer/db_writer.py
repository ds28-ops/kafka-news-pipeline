# db_writer.py
from kafka import KafkaConsumer
import json
from db.schema import Session, NewsArticle

consumer = KafkaConsumer(
    'cleaned-news',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='news-db-writer',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("DB Writer started...")
session = Session()

for msg in consumer:
    data = msg.value
    article = NewsArticle(
        link=data['link'],
        title=data['title'],
        summary=data['summary'],
        published=data['published']
    )
    # Prevent duplicates by checking if link already exists
    if not session.query(NewsArticle).filter_by(link=article.link).first():
        session.add(article)
        session.commit()
        print(f"Saved to DB: {article.title}")
    else:
        print(f"Skipped duplicate: {article.title}")
