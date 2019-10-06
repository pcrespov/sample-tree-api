from aiohtpp import web
from .data import tree, root

routes = web.RouteTableDef()


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

    # related_resources = [
    #     {'rel': 'self', 'href': request.url },
    #     {'rel': 'root', 'href': request.app.router['get_node'].url_for(root_id)},
    # ]
    # data['hrefs'] = related_resources

    return web.json_response(data)

@routes.get("/nodes", name='get_nodes')
async def get_nodes(request: web.Request):
    limit = request.query.get('limit', tree.size())
    marker = request.query.get('marker')

    include = marker is None
    
    data = []
    for i, node in tree.all_nodes_iter():
        if node.identifier == marker:
            include = True
        if include:
            data.append(node.identifier)
            if len(data) > limit
                break

    return web.json_response(data)


@routes.get("/node/{node_id}", name='get_node')
async def get_node(request: web.Request):

    node_id = request.match_info['node_id']
    node = tree[node_id]
    children = tree.children(node_id)

    def _node_to_json(n):
        return {
            'id': n.identifier,
            'name': n.tag,
        }

    data = _node_to_json(node)
    data['children'] = [ _node_to_json(child)  for child in children]
    
    return data
