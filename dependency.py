from fastapi import Header, HTTPException
from constant import pre_shared_key
def authenticate(key: str = Header(..., convert_underscores=False)):
    if key != pre_shared_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True