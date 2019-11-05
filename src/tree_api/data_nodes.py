""" Special nodes to bind s4l properties defining data

"""

import sys
from io import StringIO

import fastjsonschema
from treelib import Node, Tree

from XCore import PropertyReal, XObject
from XCoreModeling import Entity, EntityProperties

_registry = set()

def register(cls):
  assert issubclass(cls, Node)
  _registry.add(cls)
  return cls

# >>> print(brick.Properties.DumpTree())
# Block 1                                           <class 'XCoreModeling.EntityProperties'>
#     Name                                          <class 'XCore.XObject'>
#     Visible                                       <class 'XCore.PropertyBoolBinder'>
#     Color                                         <class 'XCore.XObject'>
#     Opacity                                       <class 'XCore.XObject'>
#     Transformation                                <class 'XCore.XObject'>
#         Scaling                                   <class 'XCoreMath.PropertyVec3'>
#         Rotation                                  <class 'XCoreMath.PropertyVec3'>
#         Translation                               <class 'XCoreMath.PropertyVec3'>
#     Parameters                                    <class 'XCore.PropertyGroup'>
#         SizeX                                     <class 'XCore.PropertyReal'>
#         SizeY                                     <class 'XCore.PropertyReal'>
#         SizeZ                                     <class 'XCore.PropertyReal'>
#         Centered                                  <class 'XCore.PropertyBool'>
#     Material                                      <class 'XCore.PropertyGroup'>
#         Assign                                    <class 'XCore.PropertyButton'>
#


class PropertyNode(Node):
  def __init__(self, xobj, order):
    super().__init__(tag=xobj.Name, identifier=xobj.Name)
    assert self.test(xobj), f"{self.__class__.__name__} does not pass test for {xobj}"

    self.order = order
    self._p = xobj
    self.validate = None

  def to_schema(self):
    return {
      'title': self._p.Description or "",
      'description': self._p.ToolTip or "",
      'readOnly': self._p.ReadOnly,
    }

  @classmethod
  def test(cls, xobj):
    """ True if xobj matches bind criteria"""
    return xobj is not None


@register
class GroupNode(PropertyNode):
  @classmethod
  def test(cls, xobj):
    return isinstance(xobj, EntityProperties) or \
      (isinstance(xobj, XObject) and xobj.Size>0)

  def to_schema(self):
    schema = PropertyNode.to_schema(self)
    schema.update({
      'type': 'object',
      'properties': {}
    })
    return schema


@register
class RealQuantityNode(PropertyNode):
  @classmethod
  def test(cls, xobj):
    return isinstance(xobj, PropertyReal)

  def to_schema(self):
    schema = PropertyNode.to_schema(self)
    schema.update({
      'type': 'object',
      'properties': {
            'value': {
              'type': 'number',
              'minimum': self._p.Min,
              'maximum': self._p.Max
            },
            'unit': {
              'type': 'string',
              'default': None
            }
      },
      'required': ['value',]
    })

    # TODO: Creates validator on the fly
    self.validate = fastjsonschema.compile(schema)

    # TODO: cache??
    # TODO: meta-validator or generated
    # TODO: compile data-validator?
    return schema

  def from_schema(self, branch):
    # TODO: validate json schema?? Meta-validator?
    # check if changes with previous schema
    # update prop
    #
    pass

  def to_data(self):
    data = {
      'value': self._p.Value,
      'unit': str(self._p.Unit) # TODO: do not transmit if None
    }
    # TODO: call schema validator?
    return data

  def from_data(self, branch):
    pass

  def to_uischema(self):
    ui_schema = {
      "ui:widget": "quantity3"
    }
    return ui_schema

  def from_uischema(self, branch):
    pass


# -------------------------------

def find_node_cls(obj):
  try:
    node_cls = next(cls for cls in _registry if cls.test(obj) )
  except StopIteration:
    return PropertyNode
  else:
    return node_cls

def create_data_tree(entity: Entity) -> Tree:
  tree = Tree()

  def create_node(obj: XObject, parent_id: str, order: int):
    node_cls = find_node_cls(obj)
    if node_cls:
      node = node_cls(obj, order)
      tree.add_node(node, parent=parent_id)

    # XObject interface
      if obj.Size >0:
        for i, child in enumerate(obj.Children):
          create_node(child, node.identifier, i)

  prop = entity.Properties
  create_node(prop, None, order=0)

  return tree

def get_tree_as_string(tree: Tree) -> str:
  keep = sys.stdout
  msg = ""
  try:
    sys.stdout = StringIO()
    tree.show(key=lambda n: n.order)
    msg = sys.stdout.getvalue().strip()
  finally:
    sys.stdout = keep
  return msg
