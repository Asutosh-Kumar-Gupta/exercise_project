from pydantic import BaseModel


class KeyValueInput(BaseModel):
    key: str
    value: str