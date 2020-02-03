""" Special nodes to bind s4l properties defining data

"""
from typing import Dict, List

import fastjsonschema
from treelib import Node, Tree

from XCore import (PropertyBool, PropertyColor, PropertyReal, PropertySlider,
                   PropertyString, XObject)
from XCoreMath import PropertyVec3
from XCoreModeling import Entity, EntityProperties

_registry = set()


def register(cls):
    assert issubclass(cls, Node)
    _registry.add(cls)
    return cls

# >>> print(brick.Properties.DumpTree())
# Block 1                                           <class 'XCoreModeling.EntityProperties'>
#     Name                                          <class 'XCore.PropertyStdStringBinder'>
#     Visible                                       <class 'XCore.PropertyBoolBinder'>
#     Color                                         <class 'XCore.PropertyBinderColor'>
#     Opacity                                       <class 'XCore.PropertyBinderSlider'>
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


class PropertyNode(Node):
    def __init__(self, xobj, order):
        super().__init__(tag=xobj.Name, identifier=xobj.Name)
        assert self.test(
            xobj), f"{self.__class__.__name__} does not pass test for {xobj}"

        self.order = order
        self._prop = xobj
        self.validate = None

    def getattr(self, attrname):
        if hasattr(self._prop, attrname):
            return getattr(self._prop, attrname)
        return None

    @classmethod
    def _prune(cls, data: Dict):
        return {key: value for key, value in data.items() if value not in [None, ""]}

    def to_schema(self):
        # TODO: alternatives are really verbose. add as option
        schema = {
            'title': self.getattr("Description"),
            'description': self.getattr("ToolTip"),
            'readOnly': self.getattr("ReadOnly") or False,
            'type': 'unknown'
        }
        return self._prune(schema)

    def to_uischema(self):
        ui_schema = {
            "ui:icon": self.getattr("Icon")
        }
        return self._prune(ui_schema)

    def to_data(self):
        return {}

    def from_schema(self, branch):
        # TODO: validate json schema?? Meta-validator?
        # check if changes with previous schema
        # update prop
        #
        pass

    def from_data(self, branch):
        pass

    def from_uischema(self, branch):
        pass

    @classmethod
    def test(cls, xobj):
        """ True if xobj matches bind criteria"""
        return xobj is not None


@register
class GroupNode(PropertyNode):
    @classmethod
    def test(cls, xobj):
        return isinstance(xobj, EntityProperties) or \
            (isinstance(xobj, XObject) and xobj.Size > 0)

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
        schema = super().to_schema()
        schema.update({
            'type': 'object',
            'properties': {
                'value': {
                    'type': 'number',
                    'minimum': self._prop.Min,
                    'maximum': self._prop.Max
                },
                'unit': {
                    'type': 'string',
                    'default': None
                }
            },
            'required': ['value', ]
        })

        # TODO: Creates validator on the fly
        self.validate = fastjsonschema.compile(schema)

        # TODO: cache??
        # TODO: meta-validator or generated
        # TODO: compile data-validator?
        return schema

    def to_data(self):
        data = {
            'value': self._prop.Value,
            'unit': str(self._prop.Unit)  # TODO: do not transmit if None
        }
        # TODO: call schema validator?
        return self._prune(data)

    def to_uischema(self):
        ui_schema = super().to_uischema()
        ui_schema.update({
            "ui:widget": "range" if isinstance(self._prop, PropertySlider) else "quantity"
        })
        return ui_schema


@register
class StringNode(PropertyNode):
    @classmethod
    def test(cls, xobj):
        return any(isinstance(xobj, c) for c in (PropertyString,))

    def to_schema(self):
        schema = super().to_schema()
        schema.update({
            'type': 'string',
        })
        return schema

    def to_data(self):
        return self._prop.Value

    def to_uischema(self):
        ui_schema = super().to_uischema()
        ui_schema.update({
            "ui:widget": "textarea"
        })
        return ui_schema


@register
class ColorNode(PropertyNode):
    @classmethod
    def test(cls, xobj):
        return isinstance(xobj, PropertyColor)

    def to_schema(self):
        schema = super().to_schema()
        schema.update({
            "type": "array",
            "items": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
            },
            "minItems": 4,
            "maxItems": 4
        })
        return schema

    def to_data(self):
        # TODO: call schema validator?
        c = self._prop.Value
        return [c.Red, c.Green, c.Blue, 1.0]

    def to_uischema(self):
        ui_schema = super().to_uischema()
        ui_schema.update({
            "ui:widget": "colorpicker"
        })
        return ui_schema


@register
class BoolNode(PropertyNode):
    @classmethod
    def test(cls, xobj):
        return isinstance(xobj, PropertyBool)

    def to_schema(self):
        schema = super().to_schema()
        schema.update({
            'type': 'boolean',
            'default': PropertyBool().Value if isinstance(self._prop, PropertyBool) else True
        })
        return schema

    def to_data(self):
        return self._prop.Value

    def to_uischema(self):
        ui_schema = super().to_uischema()
        ui_schema.update({
            "ui:widget": "checkbox"
        })
        return ui_schema


@register
class Vec3Node(PropertyNode):
    @classmethod
    def test(cls, xobj):
        return isinstance(xobj, PropertyVec3)

    def to_schema(self):
        schema = super().to_schema()
        schema.update({
            "type": "object",
            "properties": {
                "value": {
                    "type": "array",
                    "items": {
                      "type": "number"
                      },
                    "minItems": 3,
                    "maxItems": 3
                },
                "unit": {
                    "type": "string",
                    "default": None
                }
            },
            "required": [
                "value"
            ]
        })
        return schema

    def to_data(self):
        data = {
            'value': list(self._prop.Value),
            'unit': str(self._prop.Unit)  # TODO: do not transmit if None
        }
        # TODO: call schema validator?
        return data

    def to_uischema(self):
        ui_schema = super().to_uischema()
        ui_schema.update({
            "ui:widget": "quantity3"
        })
        return ui_schema


# Helpers -------------------------------

def find_node_cls(obj: XObject) -> PropertyNode:
    try:
        node_cls = next(cls for cls in _registry if cls.test(obj))
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
            if obj.Size > 0:
                for i, child in enumerate(obj.Children):
                    create_node(child, node.identifier, i)

    prop = entity.Properties
    create_node(prop, None, order=0)

    return tree


def tree_to_schema(tree: Tree):
    def children(node):
        for nid in node.fpointer:
            yield tree[nid]

    def to_schema(node):
        ntag = node.tag
        nschema = node.to_schema()
        for child in children(node):
            nschema['properties'].update(to_schema(child))
        return {ntag: nschema}

    schema = to_schema(tree[tree.root])
    return schema


def tree_to_uischema(tree: Tree):
    def children(node: Node) -> List[Node]:
        for nid in node.fpointer:
            yield tree[nid]

    def to_uischema(node: Node) -> Dict:
        ntag = node.tag
        nschema = node.to_uischema()
        for child in children(node):
            nschema.update(to_uischema(child))
        return {ntag: nschema}

    schema = to_uischema(tree[tree.root])
    return schema


def tree_to_data(tree: Tree):
    def children(node: Node) -> List[Node]:
        for nid in node.fpointer:
            yield tree[nid]

    def to_data(node: Node) -> Dict:
        ntag = node.tag
        ndata = node.to_data()
        for child in children(node):
            ndata.update(to_data(child))
        return {ntag: ndata}

    data = to_data(tree[tree.root])
    return data
