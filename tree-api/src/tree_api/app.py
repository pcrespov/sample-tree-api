import asyncio
import logging
from pathlib import Path

import click
import pkg_resources
from aiohttp import web
from aiohttp_swagger import setup_swagger

from . import package_name
from .data_sources import setup_data
from .handlers import routes
from .kernel import setup_kernel

log = logging.getLogger(__name__)


@click.command()
@click.option("--port", default=8080)
@click.option("--log_level", default="DEBUG")
# TODO: convert to Path?
@click.option("--data_folder", default="~/data", type=Path)
def main(port, log_level, data_folder: Path):

    logging.basicConfig(level=getattr(logging, log_level))
    log.info("Starting application ...")

    app = web.Application()
    app.add_routes(routes)

    setup_kernel(app)
    setup_data(app, data_folder.expanduser())
    setup_swagger(app,
                  swagger_from_file=pkg_resources.resource_filename(
                      package_name, 'openapi.yml'),
                  swagger_url="/doc")

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    web.run_app(app, port=port)
