import collections
import json
from pathlib import Path
from typing import Dict, Optional

import fastjsonschema
import yaml

## import jsonschema

def load_compact_schema(schema_path):
  # loads
  with schema_path.open() as fh:
    schema = yaml.safe_load(fh)

  # resolves $ref
  resolver = fastjsonschema.RefResolver(schema_path.as_uri(), schema)

  def _do_resolve(node):
    if isinstance(node, collections.Mapping) and '$ref' in node:
      with resolver.resolving(node['$ref']) as resolved:
        return resolved
    elif isinstance(node, collections.Mapping):
      for k, v in node.items():
        node[k] = _do_resolve(v)
    elif isinstance(node, (list, tuple)):
      for i in range(len(node)):
        node[i] = _do_resolve(node[i])
    return node

  resolved = _do_resolve(schema)
  resolved.pop("definitions")

  return resolved


def tojson(fpath: Path, data: Optional[Dict]=None):
  if data is None:
    with fpath.open() as fh:
      data = yaml.safe_load(fh)
  with fpath.with_suffix(".json").open("wt") as fh:
    json.dump(data, fh, indent=2)


def main():

  # data schema
  schema_path = Path("data-schema.yml").resolve()
  schema = load_compact_schema(schema_path)

  tojson(schema_path, schema)

  with schema_path.with_suffix(".py").open("wt") as fh:
    fh.write(fastjsonschema.compile_to_code(schema))

  # data
  data_path = Path("form-data.yml").resolve()
  with data_path.open() as fh:
    data = yaml.safe_load(fh)

  validate = fastjsonschema.compile(schema)
  validate(data)
  # jsonschema.validate(data, schema)

  tojson(data_path, data)

  # ui-schema
  ui_path = Path("ui-schema.yml").resolve()
  tojson(ui_path)



if __name__ == "__main__":
  main()
