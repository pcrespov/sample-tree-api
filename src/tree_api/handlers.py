from aiohttp import web
from .data import tree, root, Node
from yarl import URL

routes = web.RouteTableDef()

def _get_node_url(identifier: str, request: web.Request) -> str:
    base = request.url.origin()
    url = URL.join(base, request.app.router['get_node'].url_for(node_id=identifier))
    return str(url)


@routes.get("/", name='get_tree')
async def get_tree(request: web.Request):
    
    root_id = root.identifier

    # Building data
    data = {
        'root': root_id
    }

    # timestamps = {
    #     'created':
    #     'lastModified':
    # }
    # data.update(timestamps)

    related_resources = [
         {'rel': 'self', 'href': str(request.url) },
         {'rel': 'root', 'href': _get_node_url(root_id, request)}
    ]
    data['hrefs'] = related_resources

    return web.json_response(data)

@routes.get("/nodes", name='get_nodes')
async def get_nodes(request: web.Request):
    limit = request.query.get('limit', tree.size())
    marker = request.query.get('marker')

    include = marker is None
    
    data = []
    for node in tree.all_nodes_itr():
        if node.identifier == marker:
            include = True
        if include:
            data.append(node.identifier)
            if len(data) > limit:
                break

    return web.json_response(data)


@routes.get("/nodes/{node_id}", name='get_node')
async def get_node(request: web.Request):
    node_id = request.match_info['node_id']
    node = tree[node_id]

    parent = tree.parent(node_id)
    children = tree.children(node_id)

    # Data    
    def _node_to_json(n):
        return {
            'id': n.identifier,
            'name': n.tag,
            'href': _get_node_url(n.identifier, request)
        } if n else None

    data = _node_to_json(node)
    data['children'] = [ _node_to_json(child)  
        for child in children]
    data['parent'] = _node_to_json(parent)

    return web.json_response(data)
