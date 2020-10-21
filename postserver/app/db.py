import os

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, create_engine
from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)

metadata = MetaData()

posts_table = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50), nullable=False),
    Column("body", String(500), nullable=False),
    Column("author", String(30), nullable=False),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)
