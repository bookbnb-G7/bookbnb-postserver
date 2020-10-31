import os

# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy Engine that will interact PostgreSQL database
engine = create_engine(DATABASE_URL)

# base class for our classes definitions.
Base = declarative_base()

# SQLAlchemy ORM session factory bound to this engine 
Session = sessionmaker(bind=engine)
session = Session()
