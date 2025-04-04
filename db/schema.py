# schema.py
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///news.db')  # Use PostgreSQL/MySQL here in future
Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'articles'

    link = Column(String, primary_key=True)
    title = Column(Text)
    summary = Column(Text)
    published = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
