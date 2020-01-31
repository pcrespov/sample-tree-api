""" smash kernel

"""
from typing import Optional

from aiohttp import web
from functools import lru_cache

from pysmash.application import run_application, close_application
from XCoreModeling import Entity, GetActiveModel

APP_KERNEL_KEY = __name__


def setup_kernel(app: web.Application):
  smash_app = run_application(close_at_exit=False)
  assert smash_app is not None

  app[APP_KERNEL_KEY] = smash_app

  find_entity.cache_clear()

  async def close(_app):
    close_application()

  app.on_shutdown.append(close)


@lru_cache()
def find_entity(identifier: str) -> Optional[Entity]:
  try:
    return next( e for e in GetActiveModel().GetEntities() if str(e.Id) == identifier)
  except StopIteration:
    return None