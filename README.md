# 📰 Kafka News Pipeline

A professional, modular backend pipeline built with Apache Kafka that:

- Streams live RSS news headlines using `feedparser`
- Preprocesses and cleans the data
- Forwards cleaned data into a second Kafka topic
- Persists cleaned news into a database (SQLite for now)

This project is designed to simulate real-time stream processing pipelines in production — extensible to ML integration and web dashboards.

---

## 📦 Architecture

```
[Producer: RSS Feed]
   ↓
Kafka Topic: raw-news
   ↓
[Consumer: Cleaner]
   ↓
Kafka Topic: cleaned-news
   ↓
[Consumer: DB Writer]
   ↓
SQLite (or PostgreSQL)
```

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/ds28-ops/kafka-news-pipeline.git
cd kafka-news-pipeline
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Kafka via Docker
```bash
docker-compose up -d
```

### 4. Create Kafka topics
```bash
docker exec -it kafka-news-pipeline_kafka_1 bash

# Inside the container:
kafka-topics --bootstrap-server localhost:9092 --create --topic raw-news --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --create --topic cleaned-news --partitions 1 --replication-factor 1
exit
```

### 5. Run the pipeline

#### Producer: Fetch news & send to `raw-news`
```bash
python producer/news_producer.py
```

#### Consumer: Clean and forward to `cleaned-news`
```bash
python consumer/cleaner_consumer.py
```

#### Consumer: Save cleaned news to DB
```bash
PYTHONPATH=. python consumer/db_writer.py
```

---

## 🧼 What We Preprocess

- Remove HTML tags from summaries
- Normalize whitespace
- Format publish date to ISO8601
- Remove duplicates based on news `link`

---

## 🗃️ Database

- Default: `SQLite (news.db)` via SQLAlchemy
- Extensible to: PostgreSQL / MySQL / MongoDB

Schema:
```python
class NewsArticle(Base):
    __tablename__ = 'articles'
    link = Column(String, primary_key=True)
    title = Column(Text)
    summary = Column(Text)
    published = Column(String)
```

---

## 📁 Project Structure

```
kafka-news-pipeline/
├── consumer/
│   ├── cleaner_consumer.py
│   ├── db_writer.py
├── db/
│   ├── schema.py
│   └── __init__.py
├── producer/
│   └── news_producer.py
├── docker-compose.yml
├── news.db
```



---

## 🛠️ Built With

- Apache Kafka
- Python (`kafka-python`, `feedparser`, `sqlalchemy`)
- Docker & Docker Compose
- SQLAlchemy ORM

---




