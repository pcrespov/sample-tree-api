# pylint:disable=wildcard-import
# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
import pytest
from pysmash.application import managed_application

from tree_api.data_nodes import create_data_tree, get_tree_as_string
from XCoreModeling import (CreateSolidBlock, Entity, GetActiveModel,
                           Vec3)

import logging

logging.basicConfig(level=logging.DEBUG)


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


from textwrap import dedent


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
  got = get_tree_as_string(data_tree)
  assert  got.strip()== expected.strip()



  # Use only the interface of

  # data

  # ui-schema

#
