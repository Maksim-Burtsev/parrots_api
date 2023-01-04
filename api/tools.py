from datetime import date, datetime

from playhouse.shortcuts import model_to_dict


def obj_to_dict(model, *args, **kwargs) -> dict:
    data = model_to_dict(model, *args, **kwargs)
    for key, val in data.items():
        if isinstance(data[key], (date, datetime)):
            data[key] = str(val)
    return data
