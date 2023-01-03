from models import Breed, BreedSchema, Parrot, ParrotSchema
from sanic import Sanic
from sanic.response import json
from sanic_ext import validate

app = Sanic('parrots')


@app.route('/create_breed')
@validate(json=BreedSchema)
async def create_breed(request, body: BreedSchema):
    obj, created = Breed.update_or_create(body)
    return json({'created': created, 'id': obj.id})


@app.route('/create_parrot')
@validate(json=ParrotSchema)
async def create_parrot(request, body: ParrotSchema):
    obj = Parrot.create_obj(body)
    return json({'id': obj.id})


if __name__ == '__main__':
    app.run(auto_reload=True, debug=True)
