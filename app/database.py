from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.constans import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    modo = Column(String, default="flexible")  # New column, replaces 'type'
    hora_fija = Column(String)  # New column, replaces 'hour'


if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # Maintain a pool of 10 connections
    max_overflow=20,  # Allow up to 20 additional connections if the pool is exhausted
    pool_recycle=3600,  # Recycle connections older than one hour
)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
