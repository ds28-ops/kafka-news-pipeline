# news_producer.py
from kafka import KafkaProducer
import feedparser
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

RSS_FEED = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"

while True:
    feed = feedparser.parse(RSS_FEED)
    for entry in feed.entries[:5]:  # only take 5 at a time
        article = {
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link,
            "published": entry.published
        }
        producer.send("raw-news", value=article)
        print(f"Sent: {article['title']}")
        time.sleep(1)  # 1 sec gap between sends
    print("Sleeping for 60 seconds...\n")
    time.sleep(60)  # Fetch every minute
