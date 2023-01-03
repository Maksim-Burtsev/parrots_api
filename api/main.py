from models import Breed, BreedSchema
from sanic import Sanic
from sanic.response import json
from sanic_ext import validate

app = Sanic('parrots')


@app.route('/create_breed')
@validate(json=BreedSchema)
async def create_breed(request, body: BreedSchema):
    Breed.update_or_create(body)
    return json({'ok': True})


if __name__ == '__main__':
    app.run(auto_reload=True, debug=True)
