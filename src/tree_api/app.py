from aiohttp import web
from aiohttp_swagger import setup_swagger

from .handlers import routes

from aiohttp_swagger import setup_swagger

def main():
    app = web.Application()
    app.add_routes(routes)

    setup_swagger(app,
                  swagger_from_file="openapi.yml",
                  swagger_url="/api/v1/doc")

    web.run_app(app)
