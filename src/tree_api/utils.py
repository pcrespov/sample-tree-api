
from aiohttp import web
from treelib import Tree, Node
from typing import Dict

from .data_sources import DATA_NAMESPACE

from yarl import URL

def get_node_url(identifier: str, request: web.Request) -> str:
  base = request.url.origin()
  url = URL.join(base, request.app.router['get_node'].url_for(node_id=identifier))
  return str(url)


def get_tree(request: web.Request):
  # FIXME: check header!!!
  # FIXME: load this specific tree!? <<====
  # FIXME: format?
  tree_id = request.query.get('host')

  # FIXME: should load tree specified in host!
  tree = request.app[f"{DATA_NAMESPACE}.tree"]
  return tree


def get_metadata(node: Node, tree: Tree, *, \
    include_count=True,
    include_attrs=False,
    include_depth=True) -> Dict:
  data = {
    'id': node.identifier,
    'tag': node.tag
  }
  if include_count:
    data['childrenCount'] = len( tree.children(node.identifier) or [] )

  if include_depth:
    data['depth'] = tree.depth(node)

  if include_attrs:
    data.update(get_attributes(node))

  return data


def get_attributes(node: Node) -> Dict:
  # TODO: move to node.data! payload
  try:
    e = node.entity
    data = {
      'expanded': e.Expanded if hasattr(e, "Expanded") else True,
      'checked': e.Selected,
      'visible': e.Visible,
    }

  except Exception: #pylint: disable=broad-except
    # FIXME: add upon creation instead
    num = ord(node.identifier.split('-')[0][-1])
    data = {
      'expanded': node.expanded,
      'checked': bool(num % 3 ),  # getattr(node, 'checked', False),
      'locked':  bool(num % 2 )   #getattr(node, 'locked', False)
    }

  return data