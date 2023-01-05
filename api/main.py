from models import Breed, BreedSchema
from sanic import Sanic
from sanic.response import json
from sanic_ext import validate
from schemas import BreedDetailSchema, QueryParam
from tools import obj_to_dict

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
    data = [obj_to_dict(breed, backrefs=query.backrefs) for breed in breeds]
    return json({'result': data})


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
    obj.save()
    return json(obj_to_dict(obj))


if __name__ == '__main__':
    app.run(auto_reload=True, debug=True)
