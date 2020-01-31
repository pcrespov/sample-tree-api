from yarl import URL
from .data_sources import Node


def create_hrefs(request, *, root=None, owner=None, parent=None,
  data=None, attributes=None, nodes=False, home=False, projects=False,
  self_override: Node=None):
  base = request.url.origin()

  hrefs = {
    'self': str(request.url)
  }
  if self_override: #
    hrefs['self'] = str(URL.join(base, request.app.router['get_node'].url_for(node_id=self_override.identifier)))

  if home:
    hrefs['home'] = str(URL.join(base, request.app.router['get_home'].url_for()))

  if root:
    hrefs['root'] = str(URL.join(base, request.app.router['get_node'].url_for(node_id=root)))

  if projects:
    hrefs['projects'] = str(URL.join(base, request.app.router['get_projects'].url_for()))

  if nodes:
    hrefs['nodes'] = str(URL.join(base, request.app.router['get_nodes'].url_for()))

  if owner:
    hrefs['owner'] = str(URL.join(base, request.app.router['get_node'].url_for(node_id=owner)))

  if parent:
    hrefs['parent'] = str(URL.join(base, request.app.router['get_node'].url_for(node_id=parent)))

  if data:
    hrefs['data'] = str(URL.join(base, request.app.router['get_node_data'].url_for(node_id=data)))

  if attributes:
    hrefs['attributes'] = str(URL.join(base, request.app.router['get_node_attributes'].url_for(node_id=attributes)))
  return hrefs


def get_collection_page(nodes_iterable, marker, limit):
  nodes = []
  # TODO: refactor. if marker, exhaust iterator and if limit nodes[found:found+limit]
  include = marker is None
  for node in nodes_iterable:
    if node.identifier == marker:
      include = True
    if include:
      nodes.append(node)
      if limit <= len(nodes):
        break
  return nodes

