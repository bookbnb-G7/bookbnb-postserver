import os

from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, Integer, Float, MetaData, String, Table, ForeignKey, create_engine

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

rooms_table = Table(
    "rooms",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("price_per_day", Float, nullable=False),
    Column("accommodation_type", String(60), nullable=False)
)

room_ratings_table = Table(
    "room_ratings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("rating", Integer, nullable=False),
    Column("reviewer", String(50), nullable=False),
    Column("reviewer_id", Integer, nullable=False),
    Column("room_id", Integer, ForeignKey('rooms.id'))
)

room_reviews_table = Table(
    "room_reviews",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("review", String(500), nullable=False),
    Column("reviewer", String(50), nullable=False),
    Column("reviewer_id", Integer, nullable=False),
    Column("room_id", Integer, ForeignKey('rooms.id'))
)

# databases query builder
database = Database(DATABASE_URL)
