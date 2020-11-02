import pytest
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, get_db

db_fd, db_fname = tempfile.mkstemp()
TESTING_DB_URL = "sqlite:///" + db_fname

engine = create_engine(TESTING_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_testing_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def test_app():
	app.dependency_overrides[get_db] = get_testing_db
	client = TestClient(app)
	yield client  # testing happens here
