""" Access to database

"""
from typing import Dict, Union

from . import nodes_schemas as schemas

from fastapi.encoders import jsonable_encoder
# db
# import .nodes_modelas as models


stored = {
    0: {
        'name': 'foo'
    }
}

def get_node(idr: int):
    return stored[idr]

def set_node(idr: int, data: Union[Dict,schemas.Node] ):
    global stored ## pylint: disable=global-statement
    if isinstance(data, schemas.Node):
        data = jsonable_encoder(data)

    stored[idr] = data
