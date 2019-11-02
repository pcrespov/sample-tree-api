""" smash kernel

"""
from aiohttp import web

from pysmash.application import run_application

APP_KERNEL_KEY = __name__


def setup_kernel(app: web.Application):
  smash_app = run_application(force_standalone=True)

  app[APP_KERNEL_KEY] = smash_app
