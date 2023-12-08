# Define the database model
from sqlalchemy import Column, Integer, String
from database import Base


class KeyValue(Base):
    __tablename__ = "key_values"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True)
    value = Column(String)