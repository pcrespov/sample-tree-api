import fastjsonschema
from treelib import Node

from XCore import PropertyReal


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
  def __init__(self, xobj):
    super(PropertyNode).__init__(self)
    assert self.test(xobj), f"{self.__class__.__name__} does not pass test for {xobj}"

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
    # self.validate = fastjsonschema.compile(schema)

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


_registry = [RealQuantityNode, ]


def find(obj):
  try:
    node = next(b for b in _registry if b.test(obj) )
  except StopIteration:
    return None
  else:
    return node
