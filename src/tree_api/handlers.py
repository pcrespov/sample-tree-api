import yaml
from aiohttp import web
from yarl import URL

from .data import DATA_NAMESPACE, Node

routes = web.RouteTableDef()


def _get_node_url(identifier: str, request: web.Request) -> str:
    base = request.url.origin()
    url = URL.join(base, request.app.router['get_node'].url_for(node_id=identifier))
    return str(url)


def _get_tree(request: web.Request):
    # FIXME: check header!!!
    # FIXME: load this specific tree!?
    # FIXME: format?
    tree_id = request.query.get('host')

    # FIXME: should load tree specified in host!
    tree = request.app[f"{DATA_NAMESPACE}.tree"]
    return tree


def _get_node_attributes(node):
    data = {
        'expanded': node.expanded,
        'checked': getattr(node, 'checked', False),
        'locked': getattr(node, 'locked', False)
    }
    return data


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
    tree = _get_tree(request)

    # Building data
    data = {
        'name': tree.name,
        'root': tree.root,
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
    tree = _get_tree(request)

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
    tree = _get_tree(request)

    node_id = request.match_info['node_id']
    
    node = tree[node_id]
    parent = tree.parent(node_id)
    children = tree.children(node_id) or [] # TODO: optimize since only need number of children!

    data = {
        'id': node.identifier,
        'name': node.tag,
        'childrenCount': len(children),
        'depth': tree.depth(node),
        'href': _get_node_url(node.identifier, request)
    }

    data['hrefs'] = _create_basic_hrefs(request).pop()
    base = request.url.origin()
    
    data['hrefs'].append({'ref': 'parent', 'href': _get_node_url(parent.identifier, request) if parent else None})

    children_url = str(URL.join(base, request.app.router['get_node_children'].url_for(node_id=node.identifier)))
    data['hrefs'].append({'ref': 'children', 'href': children_url})
    
    data_url = str(URL.join(base, request.app.router['get_node_data'].url_for(node_id=node.identifier)))
    data['hrefs'].append({'ref': 'data', 'href': data_url})

    data_url = str(URL.join(base, request.app.router['get_node_attributes'].url_for(node_id=node.identifier)))
    data['hrefs'].append({'ref': 'attributes', 'href': data_url})

    return web.json_response(data)


@routes.get("/nodes/{node_id}/children", name='get_node_children')
async def get_node_children(request: web.Request):
    tree = _get_tree(request)

    node_id = request.match_info['node_id']
    node = tree[node_id]
    parent = tree.parent(node_id)
    children = tree.children(node_id) or []

    # Response
    def _to_json(anode):
        return {
            'id': anode.identifier,
            #'name': anode.tag,
            #'childrenCount': len( tree.children(anode.identifier) or [] ),
            #'depth': tree.depth(anode),
            'href': _get_node_url(anode.identifier, request)
        }

    data = {
        'children': [ _to_json(child) for child in children] or None
    }

    return web.json_response(data)

@routes.get("/nodes/{node_id}/attributes", name='get_node_attributes')
async def get_node_attributes(request: web.Request):
    tree = _get_tree(request)

    node_id = request.match_info['node_id']
    node = tree[node_id]
    attrs = _get_node_attributes(node)
    return web.json_response(data)


@routes.get("/nodes/{node_id}/data", name='get_node_data')
async def get_node_data(request: web.Request):
    
    tree = _get_tree(request)
    node_id = request.match_info['node_id']
    
    schema = yaml.safe_load("""
    type: object
    properties:
        foo: 
            type: integer
            description: 'some random integer'
        bar:
            type: number
        wo:
            type: string
        info:
            type: object
            properties:
                one:
                    type: string
                another:
                    type: string
                    description: 'something different from one'
    """)
    

    data = {
        'foo': 3,
        'bar': 3.14,
        'wo': 'a',
        'info':{
            'one': 'foo',
            'another': 'bar'
        }
    }

    return web.json_response({'data':data, 'schema':schema})
