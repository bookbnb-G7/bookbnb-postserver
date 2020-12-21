import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def test_app():
    client = TestClient(app)

    # TODO: Only for testing purpose, then use env variable
    TESTING_DB_URL = "postgresql://user:password@bookbnb-postserver_db:5432/appserver_db_dev"

    engine = create_engine(TESTING_DB_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def get_testing_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_testing_db

    yield client  # testing happens here
