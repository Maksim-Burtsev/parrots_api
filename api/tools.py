from datetime import date, datetime

from peewee import ModelSelect
from playhouse.shortcuts import model_to_dict


def obj_to_dict(model, *args, **kwargs) -> dict:
    print(args, kwargs)
    data = model_to_dict(model, *args, **kwargs)
    for key, val in data.items():
        if isinstance(data[key], (date, datetime)):
            data[key] = str(val)
    return data


def objs_to_dict(objs: ModelSelect, backrefs: bool = False) -> list[dict | None]:
    return [obj_to_dict(obj, backrefs=backrefs) for obj in objs]
