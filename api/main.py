from models import Breed, BreedSchema, Parrot
from sanic import Sanic
from sanic.response import json
from sanic_ext import validate
from schemas import BreedDetailSchema, ParrotSchema, QueryParam
from tools import obj_to_dict, objs_to_dict

app = Sanic('parrots')


@app.post('/create_breed')
@validate(json=BreedSchema)
async def create_breed(request, body: BreedSchema):
    obj, created = Breed.update_or_create(body)
    return json({'created': created, 'id': obj.id})


@app.get('/breeds')
@validate(query=QueryParam)
async def breeds(request, query: QueryParam):
    breeds = Breed.select().limit(query.limit)
    return json({'result': objs_to_dict(breeds, backrefs=query.backrefs)})


@app.get('/detail_breed/<breed_id:int>')
@validate(query=QueryParam)
async def detail_breed(request, breed_id: int, query: QueryParam):
    return json(obj_to_dict(Breed.get_or_404(breed_id), backrefs=query.backrefs))


@app.delete('/delete_breed/<breed_id:int>')
async def delete_breed(request, breed_id):
    Breed.delete_by_id(breed_id)
    return json({'status': 'ok'})


@app.patch('/update_breed/<breed_id:int>')
@validate(json=BreedDetailSchema)
async def update_breed(request, breed_id: int, body: BreedDetailSchema):
    obj = Breed.update_obj(breed_id, data=body.dict())
    return json(obj_to_dict(obj))


@app.get('/parrots')
@validate(query=QueryParam)
async def parrots(request, query: QueryParam):
    parrots = Parrot.select().limit(query.limit)
    return json({'result': objs_to_dict(parrots, backrefs=query.backrefs)})


@app.get('/detail_parrot/<parrot_id:int>')
async def detail_parrot(request, parrot_id: int):
    parrot = Parrot.get_or_404(id=parrot_id)
    return json(obj_to_dict(parrot))


@app.post('/create_parrot')
@validate(json=ParrotSchema)
async def create_parrot(request, body: ParrotSchema):
    obj, created = Parrot.update_or_create(body)
    return json({'created': created, 'id': obj.id})


@app.delete('/delete_parrot/<parrot_id:int>')
async def delete_parrot(request, parrot_id: int):
    Parrot.delete_by_id(parrot_id)
    return json({'status': 'ok'})


@app.patch('/update_parrot/<parrot_id:int>')
@validate(json=ParrotSchema)
async def update_parrot(request, parrot_id: int, body: ParrotSchema):
    parrot = Parrot.update_obj(parrot_id, data=body.dict())
    return json(obj_to_dict(parrot))


if __name__ == '__main__':
    app.run(auto_reload=True, debug=True)
