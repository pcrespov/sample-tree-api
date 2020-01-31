
from aiohttp import web
from yarl import URL

from .data_sources import DATA_NAMESPACE, Node
from .utils import get_attributes, get_metadata, get_tree
from .handlers_helpers import get_collection_page, create_hrefs


routes = web.RouteTableDef()


# TODO: schemas? marshmallow? Attrs?
# TODO: add filtering, scoping?
# TODO:

# Handlers --------------------------------------------------------------

@routes.get("/", name='get_home')
async def get_home(request: web.Request):
  tree = get_tree(request)

  data = {
    'name': tree.name, # selected project
    'root': tree.root,
    'preferences': tree.preferences,
    'hrefs': create_hrefs(request, root=tree.root, nodes=True, projects=True)
  }

  return web.json_response(data)


@routes.get("/projects", name='get_projects')
async def get_projects(request: web.Request):
  tree = get_tree(request)

  data_folder = request.app[f"{DATA_NAMESPACE}.data_folder"]
  projects = sorted(p.name for p in data_folder.glob("*.smash") )

  # TODO: add hd5 to read some metadata??

  data = {
    'projects': projects,
    'hrefs': create_hrefs(request, root=tree.root, nodes=True, home=True)
  }

  return web.json_response(data)


@routes.get("/nodes", name='get_nodes')
async def get_nodes(request: web.Request):
  tree = get_tree(request)

  # filter
  limit = int(request.query.get('limit', tree.preferences['maxItemsPerPage']))
  marker = request.query.get('marker')
  nodes = get_collection_page(tree.all_nodes_itr(), marker, limit)

  data = {
    'nodesCount': tree.size(),
    'nodes': [ get_metadata(n, tree, include_count=False) for n in nodes],
    'hrefs': create_hrefs(request, root=tree.root, home=True)
  }
  return web.json_response(data)

@routes.get("/nodes/{node_id}", name='get_node')
async def get_node(request: web.Request):
  tree = get_tree(request)

  node_id = request.match_info['node_id']

  # filter
  limit = int(request.query.get('limit', tree.preferences['maxItemsPerPage']))
  marker = request.query.get('marker')
  children = get_collection_page(tree.children(node_id) or [], marker, limit)

  # NOTE: Upon request of OM, all children folder shall have *the same* layout! I personally do not like this.
  def _build_body(anode: Node, include_children: bool):
    # NOTE: 'tree' and 'children' are taken from the outer context
    adata = get_metadata(anode, tree, include_attrs=True)

    if include_children:
      adata['children'] = [ _build_body(child, False)
        for child in children
      ] or None

    parent = tree.parent(anode.identifier)
    adata['hrefs'] = create_hrefs(request,
      root=tree.root,
      parent=parent.identifier if parent else None,
      data=anode.identifier,
      attributes=anode.identifier,
      home=True,
      self_override=anode)
    return adata

  node = tree[node_id]
  data = _build_body(node, True)

  return web.json_response(data)


@routes.get("/nodes/{node_id}/attributes", name='get_node_attributes')
async def get_node_attributes(request: web.Request):
  tree = get_tree(request)

  node_id = request.match_info['node_id']
  node = tree[node_id]
  data = get_attributes(node)

  data['hrefs'] = create_hrefs(request, owner=node_id)

  return web.json_response(data)


@routes.get("/nodes/{node_id}/data", name='get_node_data')
async def get_node_data(request: web.Request):
  tree = get_tree(request)
  node_id = request.match_info['node_id']

  assert node_id in tree

  # TODO: optimize!
  from .kernel import find_entity
  from .data_nodes import create_data_tree, tree_to_schema, tree_to_uischema, tree_to_data

  entity = find_entity(node_id)
  data_tree = create_data_tree(entity)

  data = {}
  data['schema'] = tree_to_schema(data_tree)
  data['ui'] = tree_to_uischema(data_tree)
  data['form'] = tree_to_data(data_tree)
  data['hrefs'] = create_hrefs(request, owner=node_id)

  return web.json_response(data)
