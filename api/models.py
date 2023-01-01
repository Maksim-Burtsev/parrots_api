import random
from typing import Callable

from faker import Faker
from peewee import *

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
    name = CharField(max_length=255)
    opening_time = DateTimeField(null=True)

    def generate_fake_breeds(self, count: int) -> int:
        # TODO find cite with list of them and parse it here once (its not fake for real)
        pass


class Parrot(BaseModel):
    id = AutoField()
    name = CharField()
    age = IntegerField(null=True)
    breed = ForeignKeyField(Breed, backref='parrots', null=True)

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
    Parrot.generate_fake_parrots(count=23)
