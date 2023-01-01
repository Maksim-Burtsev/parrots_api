from sanic import Sanic
from sanic_ext import validate
from schemas import ParrotSchema

app = Sanic('parrots')


@app.route('/create_parrot')
@validate(json=ParrotSchema)
async def create_parrot(request, body: ParrotSchema):
    print(body.as_dict())


if __name__ == '__main__':
    app.run(auto_reload=True, debug=True)
