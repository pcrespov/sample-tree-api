# pylint:disable=wildcard-import
# pylint:disable=unused-import
# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name

import json
from typing import Dict, Union

import pytest
from pysmash.application import run_application

from XCore import Property, PropertyBoolBinder, PropertyGroup, XObject
from XCoreModeling import (Create, CreateSolidBlock, Entity, GetActiveModel,
                           Vec3)

from . import repo_dir


@pytest.fixture(context="session")
def s4l_kernel():
  smash_app = run_application(force_standalone=True) # FIXME:teardown with session
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


import property_binder




def build_schema(obj: Union[XObject, Property]) -> Dict:
  schema = {}

  # XObject interface
  if obj.Size >0:
    schema.update({
      'type': 'object',
      'properties': {}
    })
    for child in obj.Children:
      schema['properties'][child.Name.lower()] = build_schema(child)
  else:
    node = property_binder.find(obj)


  return schema




def test_prop_to_data(entity):
  # convert Entity.Properties into

  entity.Id

  prop = entity.Properties
  schema = reference_schema
  schema = build_schema(prop)


  # Use only the interface of

  # data

  # ui-schema

#
