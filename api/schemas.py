from datetime import datetime
from typing import Any

from pydantic import BaseModel


class BreedSchema(BaseModel):
    name: str
    opening_time: datetime | None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.name = self.name.title()


class ParrotSchema(BaseModel):
    name: str
    age: int | None
    breed: str | None
