from dependency import authenticate
from fastapi import HTTPException

def test_authenticate():
    # Test successful authentication
    valid_key = "your_secret_key"
    assert authenticate(valid_key) == True

    # Test authentication failure
    invalid_key = "invalid_key"
    try:
        authenticate(invalid_key)
        assert False, "Authentication should raise an exception for an invalid key"
    except HTTPException as e:
        assert e.status_code == 401
        assert e.detail == "Invalid API key"
