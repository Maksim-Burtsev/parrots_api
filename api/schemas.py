from datetime import datetime
from typing import Any

from pydantic import BaseModel, NonNegativeInt, validator
from sanic.exceptions import SanicException


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
    breed_id: int | None

    @validator('breed_id')
    def breed_id_exists(cls, v):
        from models import Breed, ObjDoesNotExists

        try:
            Breed.get_by_id(id=v)
        except ObjDoesNotExists:
            raise SanicException('Breed does not exists', status_code=404)
        return v


class BreedDetailSchema(BaseModel):
    name: str
    opening_time: datetime | None
    parrots: list[ParrotSchema | None] | None
