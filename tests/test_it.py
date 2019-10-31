from treelib import Node, Tree
import json
import pytest

import uuid as uuidlib



@pytest.fixture
def atree():
    # view from img/treeview.png
    tree = Tree()
    tree.create_node("Model", 0) # Root
    tree.create_node("Grid", parent=0) # status = Active
    tree.create_node("Block 1", parent=0)
    group1 = tree.create_node("Group 1", parent=0)
    tree.create_node("Sphere 1", parent=group1.identifier)
    tree.create_node("Cylinder 1", parent=group1.identifier)
    return tree


import pickle

from tree_api.data_sources import create_large_tree


import yaml

def test_schemas():

    schema = yaml.safe_load("""
    type: object
    properties:
        foo:
            type: integer
            description: 'some random integer'
        bar:
            type: number
        wo:
            type: string
        info:
            type: object
            properties:
                one:
                    type: string
                another:
                    type: string
                    description: 'something different from one'
    """)
    assert schema
    # import pdb; pdb.set_trace()
    print(schema    )


def test_caching():

    tree = create_large_tree(max_depth=2, max_children=2)
    tree2 = create_large_tree(max_depth=2, max_children=2)

    import pdb; pdb.set_trace()
    tree.show()

    tree2.show()


