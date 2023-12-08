from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db  # Import the function to get the database session
from dependency import authenticate  # Import the authentication dependency
from model import KeyValue  # Import the database model
from cache import cache  # Import the caching mechanism
from schema import KeyValueInput  # Import the Pydantic model for input validation

# Create an instance of the FastAPI framework
app = FastAPI()

# Define a route for the "/ping" endpoint
@app.get("/ping")
async def ping():
    return {"message": "pong!"}  # Return a simple "pong!" message for a successful ping

# Define a route for the "/authorize" endpoint
@app.get("/authorize")
def authorize(key: str = Depends(authenticate)):
    return {"message": "Authorization successful"}  # Return a success message for authorized requests

# Define a route for the "/save" endpoint to save key-value pairs
@app.post("/save")
def save_key_value(item: KeyValueInput, db: Session = Depends(get_db)):
    # Check if the key already exists in the cache
    if item.key in cache:
        raise HTTPException(status_code=400, detail="Key already exists in the cache")

    # Check if the key already exists in the database
    existing_item = db.query(KeyValue).filter(KeyValue.key == item.key).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Key already exists in the database")

    # Create a new KeyValue instance and add it to the database
    db_item = KeyValue(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Add the key-value pair to the cache
    cache[item.key] = item.value

    return {"message": "Key-value pair saved successfully"}  # Return a success message for a successful save

# Define a route for the "/get/{key}" endpoint to retrieve values by key
@app.get("/get/{key}")
def get_value(key: str, db: Session = Depends(get_db)):
    # Check if the key exists in the cache
    cached_value = cache.get(key)
    if cached_value:
        return {"key": key, "value": cached_value}  # Return the cached value if found

    # Retrieve the value associated with the key from the database
    db_item = db.query(KeyValue).filter(KeyValue.key == key).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Key not found in the database")

    # Add the key-value pair to the cache
    cache[key] = db_item.value

    return {"key": key, "value": db_item.value}  # Return the value from the database

# Define a route for the "/delete/{key}" endpoint to delete key-value pairs
@app.delete("/delete/{key}")
def delete_key(key: str, db: Session = Depends(get_db)):
    # Delete the key-value pair from the database and the cache
    db_item = db.query(KeyValue).filter(KeyValue.key == key).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Key not found in the database")
    cache.pop(key)
    db.delete(db_item)
    db.commit()

    return {"message": f"Key '{key}' deleted successfully"}  # Return a success message for a successful deletion
