from datetime import datetime

from pydantic import BaseModel


class BreedSchema(BaseModel):
    name: str
    opening_time: datetime | None


class ParrotSchema(BaseModel):
    name: str
    age: int | None
    breed: str | None
