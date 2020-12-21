import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ENVIRONMENT = os.getenv("ENVIRONMENT")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
session = None

print(ENVIRONMENT)

if ENVIRONMENT == "production":
    engine = create_engine(DATABASE_URL)

if ENVIRONMENT == "development":
    engine = create_engine(DATABASE_URL, echo=True)

if ENVIRONMENT == "testing":
    engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Create a Base class for models
Base = declarative_base()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
