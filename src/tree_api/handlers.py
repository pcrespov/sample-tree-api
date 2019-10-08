from typing import Dict

import yaml
from aiohttp import web
from yarl import URL

from .data import DATA_NAMESPACE, Node, Tree


routes = web.RouteTableDef()
MAX_ITEMS_PER_PAGE = 20


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

def _get_node_meta(node: Node, tree: Tree, request: web.Request, *, \
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
        data.update(_get_node_attributes(node))

    if request is not None:
        data['href'] = _get_node_url(node.identifier, request)
    return data

def _get_node_attributes(node: Node) -> Dict:
    # TODO: move to node.data! payload
    data = {
        'expanded': node.expanded,
        'checked': getattr(node, 'checked', False),
        'locked': getattr(node, 'locked', False)
    }
    return data

def _create_hrefs(request, *, root=None, owner=None, parent=None, data=None, attributes=None):
    base = request.url.origin()

    hrefs = [{
        'rel': 'self', 
        'href': str(request.url) 
        }, 
    ]
    
    if root:
        hrefs.append({
            'rel': 'root', 
            'href': str(URL.join(base, request.app.router['get_node'].url_for(node_id=root)))
        })

    if owner:
        hrefs.append({
            'rel': 'owner', 
            'href': str(URL.join(base, request.app.router['get_node'].url_for(node_id=owner)))
        })

    if parent:
        hrefs.append({
            'rel': 'parent', 
            'href': str(URL.join(base, request.app.router['get_node'].url_for(node_id=parent)))
        })
    
    if data:
        hrefs.append({
            'rel': 'data', 
            'href': str(URL.join(base, request.app.router['get_node_data'].url_for(node_id=data)))
        })

    if attributes:
        hrefs.append({
            'rel': 'attributes', 
            'href': str(URL.join(base, request.app.router['get_node_attributes'].url_for(node_id=attributes)))
        })
    return hrefs

def _get_collection_page(nodes_iterable, marker, limit):
    nodes = []
    include = marker is None
    for node in nodes_iterable:
        if node.identifier == marker:
            include = True
        if include:
            nodes.append(node)
            if len(nodes) >= limit:
                break
    return nodes


# TODO: schemas? marshmallow? Attrs?
# TODO: add filtering, scoping?
# TODO: 

# Handlers ------------

@routes.get("/", name='get_tree')
async def get_tree(request: web.Request):
    tree = _get_tree(request)

    data = {
        'name': tree.name,
        'root': tree.root,
        'hrefs': _create_hrefs(request, root=tree.root)
    }

    return web.json_response(data)

@routes.get("/nodes", name='get_nodes')
async def get_nodes(request: web.Request):
    tree = _get_tree(request)

    # filter
    limit = int(request.query.get('limit', MAX_ITEMS_PER_PAGE))
    marker = request.query.get('marker')
    nodes = _get_collection_page(tree.all_nodes_itr(), marker, limit)

    data = {
        'nodes': [ _get_node_meta(n, tree, None, include_count=False) for n in nodes],
        'hrefs': _create_hrefs(request, root=tree.root)
    }
    return web.json_response(data)

@routes.get("/nodes/{node_id}", name='get_node')
async def get_node(request: web.Request):
    tree = _get_tree(request)

    node_id = request.match_info['node_id']

    node = tree[node_id]
    data = _get_node_meta(node, tree, None, include_attrs=True)

    # filter
    limit = int(request.query.get('limit', MAX_ITEMS_PER_PAGE))
    marker = request.query.get('marker')
    children = _get_collection_page(tree.children(node_id) or [], marker, limit)

    data['children'] = [ _get_node_meta(child, tree, request, include_attrs=True, include_depth=False)
        for child in children
    ] or None

    parent = tree.parent(node_id)
    data['hrefs'] = _create_hrefs(request,
        root=tree.root, 
        parent=parent.identifier if parent else None, 
        data=node_id, 
        attributes=node_id)

    return web.json_response(data)


@routes.get("/nodes/{node_id}/attributes", name='get_node_attributes')
async def get_node_attributes(request: web.Request):
    tree = _get_tree(request)

    node_id = request.match_info['node_id']
    node = tree[node_id]
    data = _get_node_attributes(node)

    data['hrefs'] = _create_hrefs(request,
        owner=node_id)

    return web.json_response(data)


@routes.get("/nodes/{node_id}/data", name='get_node_data')
async def get_node_data(request: web.Request):    
    tree = _get_tree(request)
    node_id = request.match_info['node_id']
    
    data ={}

    #TODO:  move to data.py
    data['schema'] = yaml.safe_load("""
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
    

    data['data'] = {
        'foo': 3,
        'bar': 3.14,
        'wo': 'a',
        'info':{
            'one': 'foo',
            'another': 'bar'
        }
    }

    data['hrefs'] = _create_hrefs(request,
        owner=node_id)

    return web.json_response(data)
