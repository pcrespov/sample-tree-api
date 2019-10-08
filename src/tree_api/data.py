import functools
import logging
import os
import pickle
import random
from pathlib import Path

import attr
from aiohttp import web
from faker import Faker
from treelib import Node, Tree

fake = Faker()

DATA_NAMESPACE = __name__

log = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class Attributes:
    pass
#    created : 
#    last_modified : 
#
    # 2019-10-04T08:36:01Z



def cache_data(creator_fun):
    @functools.wraps(creator_fun)
    def decorator(**kargs):
        suffix = "x".join(map(str, kargs.values()))
        path = Path(f".tmp/{creator_fun.__name__}-{suffix}")
        if path.exists():
            log.info(f"Using cache %s", path)
            with path.open('rb') as fh:
                data = pickle.load(fh)
        else:
            data = creator_fun(**kargs)
            os.makedirs(path.parent, exist_ok=True)
            with path.open('wb') as fh:
                pickle.dump(data, fh)
        return data

    return decorator


@cache_data
def create_large_tree(*,max_depth: int=5, max_children: int=20):
    tree = Tree()
    tree.name = "large-tree"

    def create_children(parent, depth):
        if depth+1 <= max_depth:
            N = random.randrange(max_children)
            names = [ f"{fake.name()}" for n in range(N)] # n random names # pylint: disable=no-member
            children = [ tree.create_node(name, parent=parent.identifier) for name in names ]
            for child in children:
                create_children(child, depth+1)

    root = tree.create_node("root", identifier="d2746468-12dc-4fc7-8a03-2ada76b53a1e")
    create_children(root, depth=0)

    return tree


def create_sample_tree():
    # view from img/treeview.png

    # This is : small.sample.itis.swiss
    #   Model (root) 7865b1fa-e680-11e9-ba43-ac9e17b76a71
    #   ├── Block 1  d29dced4-4399-4bdc-951d-d474a48db477
    #   ├── Grid     5e92f325-2085-45ab-9c21-8a9019a2290d
    #   └── Group 1  17895910-9d97-45d0-aeeb-0faaff44080e
    #       ├── Cylinder 1  e7c5e7f0-a1e3-4d2a-b958-494c33923fa0
    #       └── Sphere 1    d3e0da1c-e7a4-4adb-960c-00b477cb1df5    

    tree = Tree()
    tree.name = "sample-tree"
    root = tree.create_node("model", identifier="7865b1fa-e680-11e9-ba43-ac9e17b76a71", data=Attributes()) # Root

    tree.create_node("Grid", parent=root.identifier, data=Attributes())
    tree.create_node("Block 1", parent=root.identifier, data=Attributes())

    group1 = tree.create_node("Group 1", parent=root.identifier, data=Attributes())
    tree.create_node("Sphere 1", parent=group1.identifier, data=Attributes())
    tree.create_node("Cylinder 1", parent=group1.identifier, data=Attributes())
    return tree

def setup_data(app: web.Application):
    #tree = create_sample_tree()
    log.debug("building sample tree")
    tree = create_large_tree(max_depth=4, max_children=30)
    log.debug("saving sample tree")

    app[f"{DATA_NAMESPACE}.tree"] = tree
    


__all__ = [
    'Node', 'Tree'
]
