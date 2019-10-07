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

from tree_api.data import create_large_tree


def test_caching():

    tree = create_large_tree(max_depth=2, max_children=2)
    tree2 = create_large_tree(max_depth=2, max_children=2)
    
    import pdb; pdb.set_trace()
    tree.show()

    tree2.show()


