import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.event import listen, remove


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')
    dbapi_conn.enable_load_extension(False)


DATABASE_URL = os.getenv("DATABASE_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT")


engine = None
session = None
metadata = None
Base = None
if ENVIRONMENT == "production":
    # use postgresql
    engine = create_engine(DATABASE_URL)
    Base = declarative_base()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

if ENVIRONMENT == "development":
    # use sqlite
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
    listen(engine, 'connect', load_spatialite)
    metadata = MetaData(engine)
    # Create a Base class for models
    Base = declarative_base(metadata=metadata)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    session.execute('SELECT InitSpatialMetaData(1)')
    remove(engine, 'connect', load_spatialite)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
