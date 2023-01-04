from models import Breed, BreedSchema
from playhouse.shortcuts import model_to_dict
from sanic import Sanic
from sanic.response import json
from sanic_ext import validate
from schemas import BackrefsParam

app = Sanic('parrots')


@app.route('/create_breed')
@validate(json=BreedSchema)
async def create_breed(request, body: BreedSchema):
    obj, created = Breed.update_or_create(body)
    return json({'created': created, 'id': obj.id})


@app.route('/detail_breed/<breed_id:int>')
@validate(query=BackrefsParam)
async def detail_breed(request, breed_id: int, query: BackrefsParam):
    return json(model_to_dict(Breed.get_or_404(breed_id), backrefs=query.backrefs))


@app.route('/delete_breed')
@validate(json=BreedSchema)
async def delete_breed(request):
    pass


@app.route('/update_breed')
@validate(json=BreedSchema)
async def update_breed(request):
    pass


if __name__ == '__main__':
    app.run(auto_reload=True, debug=True)
