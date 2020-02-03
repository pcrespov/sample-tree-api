""" Access to database

"""
from typing import Dict



stored = {
    0: {
        'name': 'foo'
    }
}

def get_node(idr: int):
    return stored[idr]

def set_node(idr: int, data: Dict):
    global stored
    stored[idr] = data
