# Create SQLite database engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base for database models
Base = declarative_base()

Base.metadata.create_all(bind=engine)


    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()