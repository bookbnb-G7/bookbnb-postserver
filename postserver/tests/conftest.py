import os
import pytest
from app.main import app
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.db import Base, get_db, engine, recreate_database


@pytest.fixture(scope="session", autouse=True)
def test_app():
    client = TestClient(app)

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


@pytest.fixture(scope="session", autouse=True)
def test_app():
    recreate_database()

    client = TestClient(app)

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
