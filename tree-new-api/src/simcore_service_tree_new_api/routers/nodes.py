""" Rest API methods for node

Standard Methods: https://cloud.google.com/apis/design/standard_methods

"""

from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi import Path as PathParam
from fastapi import Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

router = APIRouter()



class Node(BaseModel):
    name: str

class CollectionPage(BaseModel):
    # pagination metadata
    total_size : Optional[int]=0
    next_page_token: str="" # pagination token to retrieve the next page of results. If the value is "", it means no further results for the request.


class NodesList(CollectionPage):
    nodes: List[Node] = []



# LIST: https://cloud.google.com/apis/design/standard_methods#list

@router.get("",
    response_model=NodesList)
async def list_nodes(
    page_token: Optional[str] = Query(None, description="Requests a specific page of the list results"),
    page_size: int = Query(0, ge=0, description="Maximum number of results to be returned by the server"),
    order_by: Optional[str] = Query(None, description="Sorts in ascending order comma-separated fields")
    ):
    # List is suited to data from a single collection that is bounded in size and not cached


    # Applicable common patterns
    # SEE pagination: https://cloud.google.com/apis/design/design_patterns#list_pagination
    # SEE sorting https://cloud.google.com/apis/design/design_patterns#sorting_order

    # Applicable naming conventions
    # SEE filter: https://cloud.google.com/apis/design/naming_convention#list_filter_field
    # SEE response: https://cloud.google.com/apis/design/naming_convention#list_response

    print(page_token)
    print(page_size)
    print(order_by)


@router.get(":batchGet")
async def batch_get_nodes():
    pass

@router.get(":search")
async def search_nodes():
    # A method that takes multiple resource IDs and returns an object for each of those IDs
    # Alternative to List for fetching data that does not adhere to List semantics, such as services.search.
    #https://cloud.google.com/apis/design/standard_methods#list
    pass



# GET: https://cloud.google.com/apis/design/standard_methods#get
@router.get("/{node_id}",
    response_model=Node)
async def get_node(node_id: int):
    return Node(f"node {node_id} in collection")


# CREATE: https://cloud.google.com/apis/design/standard_methods#create
@router.post("",
    response_model=Node)
async def create_node():
    return Node("new node")

@router.post("/{node_id}",
    response_model=Node)
async def create_node_with_id(node_id: int):

    if node_id==0:
        # client-assigned resouce name
        raise HTTPException(status_code=409, detail=f"Node {node_id} already exists")

    return Node(f"new node with id {node_id}")




stored = {
    0: {
        'name': 'foo'
    }
}

# UPDATE https://cloud.google.com/apis/design/standard_methods#update
@router.patch("/{node_id}",
    response_model=Node)
async def udpate_node(node_id: int, *, node: Node):
    # load
    stored_data = stored[node_id]
    stored_obj = Node(**stored_data)

    # update
    update_data = node.dict(exclude_unset=True)
    updated_obj = stored_obj.copy(update=update_data)

    # save
    stored[node_id] = jsonable_encoder(updated_obj)

    return node


@router.delete("/{node_id}")
async def delete_node(node_id: int):
    print(f"Node {node_id} deleted")
