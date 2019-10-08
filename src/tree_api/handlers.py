from aiohttp import web
from .data import DATA_NAMESPACE, Node
from yarl import URL

routes = web.RouteTableDef()


def _get_node_url(identifier: str, request: web.Request) -> str:
    base = request.url.origin()
    url = URL.join(base, request.app.router['get_node'].url_for(node_id=identifier))
    return str(url)

def _load_tree(request: web.Request):
    # FIXME: check header!!!
    # FIXME: load this specific tree!?
    # FIXME: format?
    tree_id = request.query.get('host')

    # FIXME: should load tree specified in host!
    tree = request.app[f"{DATA_NAMESPACE}.tree"]
    return tree


def _create_basic_hrefs(request: web.Request):
    tree = request.app[f"{DATA_NAMESPACE}.tree"]
    hrefs = [
        {'rel': 'self', 'href': str(request.url) },
        {'rel': 'root', 'href': _get_node_url(tree.root, request)}
    ]
    return hrefs

# TODO: schemas? marshmallow? Attrs?


# Handlers ------------

@routes.get("/", name='get_tree')
async def get_tree(request: web.Request):
    tree = _load_tree(request)

    # Building data
    data = {
        'name': tree.name,
        'root': tree.root
    }

    # timestamps = {
    #     'created':
    #     'lastModified':
    # }
    # data.update(timestamps)

    data['hrefs'] = _create_basic_hrefs(request)

    return web.json_response(data)

@routes.get("/nodes", name='get_nodes')
async def get_nodes(request: web.Request):
    tree = _load_tree(request)

    limit = int(request.query.get('limit', tree.size()))
    marker = request.query.get('marker')

    include = marker is None
    
    nodes = []
    for node in tree.all_nodes_itr():
        if node.identifier == marker:
            include = True
        if include:
            nodes.append(node.identifier)
            if len(nodes) >= limit:
                break

    data = {
        'nodes': nodes,
        'hrefs': _create_basic_hrefs(request)
    }
    return web.json_response(data)

@routes.get("/nodes/{node_id}", name='get_node')
async def get_node(request: web.Request):
    tree = _load_tree(request)

    node_id = request.match_info['node_id']
    node = tree[node_id]

    parent = tree.parent(node_id)
    children = tree.children(node_id) or []

    # Data    
    def _to_json(anode):
        return {
            'id': anode.identifier,
            'name': anode.tag,
            'childrenCount': len( tree.children(anode.identifier) or [] ),
            'href': _get_node_url(anode.identifier, request)
        } if anode else None

    data = _to_json(node)
    data['children'] = [ _to_json(child) for child in children] or None
    data['parent'] = _to_json(parent)

    return web.json_response(data)
