import json
import random
from typing import Callable, NamedTuple

import pydantic
from faker import Faker
from loguru import logger
from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    PostgresqlDatabase,
)
from playhouse.shortcuts import update_model_from_dict
from sanic.exceptions import SanicException
from schemas import BreedSchema

DEFAULT_BREEDS_PATH = 'api/default_breeds.json'
db = PostgresqlDatabase('people', host='localhost')


class ObjDoesNotExists(Exception):
    ...


class ObjCreated(NamedTuple):
    obj: Model
    created: bool


def db_connect(func: Callable):
    def wrapper(*args, **kwargs):
        with db:
            result = func(*args, **kwargs)
        return result

    return wrapper


def create_tables():
    return db.create_tables([Parrot, Breed])


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    @db_connect
    def update_or_create(
        cls,
        data: pydantic.BaseModel,
        fields: list[str | None],
    ) -> ObjCreated:
        created = False
        try:
            obj = (
                cls.select()
                .where([getattr(cls, field) == getattr(data, field) for field in fields])
                .get()
            )
            for attr, val in data.dict().items():
                if getattr(obj, attr):
                    setattr(obj, attr, val)
            obj.save()
        except Exception as exc:
            logger.exception(exc)
            obj = cls.create(**data.dict())
            created = True

        return ObjCreated(obj, created)

    @classmethod
    @db_connect
    def create_obj(cls, data: pydantic.BaseModel) -> Model:
        return cls.create(**data.dict())

    @classmethod
    @db_connect
    def update_obj(cls, id: int, data: pydantic.BaseModel) -> Model:
        obj = cls.get_or_404(id)
        updated_obj = update_model_from_dict(obj, data)
        updated_obj.save()
        return updated_obj

    @classmethod
    def get_by_id(cls, id: int) -> Model:
        opened = False
        if db.is_closed():
            db.connect()
            opened = True
        try:
            obj = cls.select().where(cls.id == id).get()
        except Exception as exc:
            logger.info(exc)
            raise ObjDoesNotExists(f"{cls} doesn't have obj with {id=}")
        if opened:
            db.close()
        return obj

    @classmethod
    def delete_by_id(cls, id: int) -> None:
        obj = cls.get_or_404(id)
        obj.delete_instance()

    @classmethod
    @db_connect
    def get_or_404(cls, id: int) -> Model:
        try:
            obj = cls.get_by_id(id)
        except Exception as exc:
            logger.info(exc)
            raise SanicException(status_code=404)
        return obj


class Breed(BaseModel):
    id = AutoField(index=True)
    name = CharField(max_length=255, unique=True)
    opening_time = DateTimeField(null=True)

    @classmethod
    def update_or_create(cls, data: BreedSchema) -> None:
        return super().update_or_create(data, fields=['name'])

    @classmethod
    def load_default_breeds(cls) -> None:
        with open(DEFAULT_BREEDS_PATH, 'r') as f:
            raw_data = json.loads(f.read())
        data = [{'name': breed} for breed in raw_data.values()]
        cls.insert_many(data).execute()

    @classmethod
    def breed_with_parrots(cls):
        return cls.select()


class Parrot(BaseModel):
    id = AutoField(index=True)
    name = CharField()
    age = IntegerField(null=True)
    breed = ForeignKeyField(
        Breed,
        backref='parrots',
        null=True,
        on_delete='SET NULL',
        index=True,
    )

    @classmethod
    def generate_fake_parrots(
        cls,
        count: int,
        fake: Faker = Faker(),
    ) -> int:
        breed_ids = list(Breed.select(Breed.id))
        data = [
            {
                'name': fake.first_name() + 'test',
                'age': random.randint(10, 100),
                'breed_id': random.choice(breed_ids),
            }
            for _ in range(count)
        ]
        cls.insert_many(data).execute()

    @classmethod
    def update_or_create(
        cls,
        data: pydantic.BaseModel,
        fields: list[str] = ['id'],
    ) -> ObjCreated:
        return super().update_or_create(data, fields=fields)


if __name__ == '__main__':
    Parrot.generate_fake_parrots(1_000)
