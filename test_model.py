from model import KeyValue
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import pytest

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

def test_key_value_model(db: Session):
    # Test creating a KeyValue instance
    item = KeyValue(key="test_key", value="test_value")
    assert item.key == "test_key"
    assert item.value == "test_value"

    # Test saving to and retrieving from the database
    db.add(item)
    db.commit()
    db_item = db.query(KeyValue).filter(KeyValue.key == "test_key").first()
    assert db_item is not None
    assert db_item.key == "test_key"
    assert db_item.value == "test_value"
