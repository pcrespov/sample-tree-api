# pylint:disable=wildcard-import
# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
import json
import logging
from textwrap import dedent

import pytest

from pysmash.application import managed_application
from tree_api.data_nodes import create_data_tree, tree_to_schema, tree_to_uischema, tree_to_data
from XCoreModeling import CreateSolidBlock, Entity, GetActiveModel, Vec3
from treelib import Tree


logging.basicConfig(level=logging.DEBUG)

# FIXTURES ####

@pytest.fixture(scope="session")
def s4l_kernel():
  with managed_application() as smash_app:
    yield smash_app


@pytest.fixture
def s4l_modeler(s4l_kernel):
  model = GetActiveModel()
  yield model


@pytest.fixture
def entity(s4l_modeler):
  e = CreateSolidBlock(Vec3(-1), Vec3(+1), parametrized=True)
  assert isinstance(e, Entity)
  yield e
  e.Delete()

# HELPERS ####

def _get_tree_as_string(tree: Tree) -> str:
  import sys
  from io import StringIO

  keep = sys.stdout
  msg = ""
  try:
    sys.stdout = StringIO()
    tree.show(key=lambda n: n.order)
    msg = sys.stdout.getvalue().strip()
  finally:
    sys.stdout = keep
  return msg


# TESTS ####

def test_prop_to_data(entity):
  # convert Entity.Properties into
  # entity.Id

  data_tree = create_data_tree(entity)

  expected = dedent("""
  Block 1
  ├── Name
  ├── Visible
  ├── Color
  ├── Opacity
  ├── Transformation
  │   ├── Scaling
  │   ├── Rotation
  │   └── Translation
  ├── Parameters
  │   ├── SizeX
  │   ├── SizeY
  │   ├── SizeZ
  │   └── Centered
  └── Material
      └── Assign
  """)
  got = _get_tree_as_string(data_tree)
  assert  got.strip()== expected.strip()

  data_schema = tree_to_schema(data_tree)
  print(json.dumps(data_schema, indent=2))

  data_uischema = tree_to_uischema(data_tree)
  print(json.dumps(data_uischema, indent=2))

  data_data = tree_to_data(data_tree)
  print(json.dumps(data_data, indent=2))

