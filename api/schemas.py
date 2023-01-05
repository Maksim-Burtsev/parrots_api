from datetime import datetime
from typing import Any

from pydantic import BaseModel, NonNegativeInt


class QueryParam(BaseModel):
    backrefs: bool | None
    limit: NonNegativeInt | None = None


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


class BreedDetailSchema(BaseModel):
    name: str
    opening_time: datetime | None
    parrots: list[ParrotSchema | None] | None
