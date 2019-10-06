from treelib import Node, Tree
import json
import pytest

import uuid as uuidlib



@pytest.fixture
def sample_model_tree():
    # view from img/treeview.png
    tree = Tree()
    tree.create_node("Model", 0) # Root
    tree.create_node("Grid", parent=0) # status = Active
    tree.create_node("Block 1", parent=0)
    group1 = tree.create_node("Group 1", parent=0)
    tree.create_node("Sphere 1", parent=group1.identifier)
    tree.create_node("Cylinder 1", parent=group1.identifier)
    return tree


def test_get_domain(sample_model_tree):
    
    tree = sample_model_tree

    import pdb; pdb.set_trace()

    tree.show()
    
    print(json.dumps(tree.to_json(), indent=2))


    # get root
    root = tree.nodes[0]
    assert root.identifier == tree.root
    

    # get 
    



    



