from treelib import Node, Tree
import json
import pytest


@pytest.fixture
def sample_model_tree():
    # view from img/treeview.png
    tree = Tree()
    tree.create_node("Model", 0) # Root
    tree.create_node("Grid", parent=0) # status = Active
    tree.create_node("Block 1", parent=0)
    tree.create_node("Group 1", 1, parent=0)
    tree.create_node("Sphere 1", parent=1)
    tree.create_node("Cylinder 1", parent=1)
    return tree


def test_get_domain(sample_model_tree):
    
    tree.show()



    import pdb; pdb.set_trace()
    print(json.dumps(tree.to_json(), indent=2))
