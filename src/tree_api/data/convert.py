import collections
import json
from pathlib import Path

import fastjsonschema
import jsonschema
import yaml


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


def main():

    schema_path = Path("data-schema.yml").resolve()
    schema = load_compact_schema(schema_path)

    with schema_path.with_suffix(".json").open("wt") as fh:
        json.dump(schema, fh, indent=2)

    with schema_path.with_suffix(".py").open("wt") as fh:
        fh.write(fastjsonschema.compile_to_code(schema))


    # data
    data_path = Path("form-data.yml").resolve()
    with data_path.open() as fh:
        data = yaml.safe_load(fh)

    validate = fastjsonschema.compile(schema)
    validate(data)
    # jsonschema.validate(data, schema)

    with data_path.with_suffix(".json").open("wt") as fh:
        json.dump(data, fh, indent=2)


if __name__ == "__main__":
    main()
