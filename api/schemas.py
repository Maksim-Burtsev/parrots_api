from dataclasses import dataclass


@dataclass
class ParrotSchema:
    name: str
    age: int | None
    breed: str | None
