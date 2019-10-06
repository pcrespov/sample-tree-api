import pkg_resources
from aiohttp import web
from aiohttp_swagger import setup_swagger

from . import package_name
from .handlers import routes
import asyncio

def main():
    app = web.Application()
    app.add_routes(routes)

    #setup_swagger(app,
    #              swagger_from_file=pkg_resources.resource_filename(package_name, 'openapi.yml'),
    #              swagger_url="/doc")

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    web.run_app(app)
