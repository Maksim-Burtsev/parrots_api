import json
import random
from typing import Callable

from faker import Faker
from peewee import *

DEFAULT_BREEDS_PATH = 'api/default_breeds.json'
db = PostgresqlDatabase('people', host='localhost')


def db_connect(func: Callable):
    def wrapper(*args, **kwargs):
        db.connect()
        result = func(*args, **kwargs)
        db.close()
        return result

    return wrapper


def create_tables():
    return db.create_tables([Parrot, Breed])


class BaseModel(Model):
    class Meta:
        database = db


class Breed(BaseModel):
    id = AutoField()
    name = CharField(max_length=255, unique=True)
    opening_time = DateTimeField(null=True)

    @classmethod
    def load_default_breeds(cls) -> None:
        with open(DEFAULT_BREEDS_PATH, 'r') as f:
            raw_data = json.loads(f.read())
        data = [{'name': breed} for breed in raw_data.values()]
        cls.insert_many(data).execute()


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
            {'name': fake.first_name(), 'age': random.randint(10, 100)}
            for _ in range(count)
        ]
        cls.insert_many(data).execute()


if __name__ == '__main__':
    pass
