import json
import random
from typing import Callable, NamedTuple

import pydantic
from faker import Faker
from loguru import logger
from peewee import *
from sanic.exceptions import SanicException
from schemas import BreedSchema

DEFAULT_BREEDS_PATH = 'api/default_breeds.json'
db = PostgresqlDatabase('people', host='localhost')


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
        cls, data: pydantic.BaseModel, fields: list[str | None]
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
    def delete_obj(cls, id: int) -> None:
        pass

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
    id = AutoField()
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
    id = AutoField()
    name = CharField()
    age = IntegerField(null=True)
    breed = ForeignKeyField(Breed, backref='parrots', null=True, on_delete='SET NULL')

    @classmethod
    def generate_fake_parrots(
        cls,
        count: int,
        fake: Faker = Faker(),
    ) -> int:
        data = [
            {
                'name': fake.first_name() + 'test',
                'age': random.randint(10, 100),
                'breed_id': 1,
            }
            for _ in range(count)
        ]
        cls.insert_many(data).execute()

    @classmethod
    def update_or_create(
        cls, data: pydantic.BaseModel, fields: list[str] = ['id']
    ) -> ObjCreated:
        return super().update_or_create(data, fields=fields)


if __name__ == '__main__':
    print(Breed.get_or_404(10000))
