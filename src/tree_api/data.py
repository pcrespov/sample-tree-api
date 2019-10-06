import attr
from treelib import Tree, Node
# view from img/treeview.png

# This is : small.sample.itis.swiss
#   Model (root) 7865b1fa-e680-11e9-ba43-ac9e17b76a71
#   ├── Block 1  d29dced4-4399-4bdc-951d-d474a48db477
#   ├── Grid     5e92f325-2085-45ab-9c21-8a9019a2290d
#   └── Group 1  17895910-9d97-45d0-aeeb-0faaff44080e
#       ├── Cylinder 1  e7c5e7f0-a1e3-4d2a-b958-494c33923fa0
#       └── Sphere 1    d3e0da1c-e7a4-4adb-960c-00b477cb1df5

@attr.s(auto_attribs=True)
class Attributes:
    pass
#    created : 
#    last_modified : 
#
    # 2019-10-04T08:36:01Z


tree = Tree()
root = tree.create_node("Model", data=Attributes()) # Root
tree.create_node("Grid", parent=root.identifier, data=Attributes())
tree.create_node("Block 1", parent=root.identifier, data=Attributes())

group1 = tree.create_node("Group 1", parent=root.identifier, data=Attributes())
tree.create_node("Sphere 1", parent=group1.identifier, data=Attributes())
tree.create_node("Cylinder 1", parent=group1.identifier, data=Attributes())



__all__ = [
    'Node'
]