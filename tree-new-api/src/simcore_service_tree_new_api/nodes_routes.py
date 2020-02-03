""" Rest API methods for node

Standard Methods: https://cloud.google.com/apis/design/standard_methods

"""

import uuid as uuidlib
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from starlette.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                              HTTP_409_CONFLICT)

from . import nodes_crud as crud
from . import nodes_schemas as schemas

#from fastapi import Path as PathParam
#from starlette.responses import JSONResponse





router = APIRouter()


# LIST --------------
#   https://cloud.google.com/apis/design/standard_methods#list

@router.get("",
    response_model=schemas.NodesList
    )
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
    # TODO: filter: https://cloud.google.com/apis/design/naming_convention#list_filter_field
    # SEE response: https://cloud.google.com/apis/design/naming_convention#list_response

    print(page_token)
    print(page_size)
    print(order_by)


@router.get(":batchGet"
    )
async def batch_get_nodes():
    raise NotImplementedError()


@router.get(":search"
    )
async def search_nodes():
    # A method that takes multiple resource IDs and returns an object for each of those IDs
    # Alternative to List for fetching data that does not adhere to List semantics, such as services.search.
    #https://cloud.google.com/apis/design/standard_methods#list
    raise NotImplementedError()




# GET --------------
#  https://cloud.google.com/apis/design/standard_methods#get

@router.get("/{node_id}",
    response_model=schemas.Node
    )
async def get_node(node_id: int):
    return schemas.Node(f"node {node_id} in collection")




# CREATE --------------
#  https://cloud.google.com/apis/design/standard_methods#create

@router.post("",
    response_model=schemas.Node,
    status_code=HTTP_201_CREATED,
    response_description="Successfully created"
    )
async def create_node(node: schemas.NodeIn=Body(None)):
    # ...
    if node.id:
        # client-assigned resouce name
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f"Node {node.id} already exists")

    node = schemas.Node(uuidlib.uuid4(), "new")
    crud.set_node(node.id, node)
    return node




# UPDATE  --------------
# https://cloud.google.com/apis/design/standard_methods#update
@router.patch("/{node_id}",
    response_model=schemas.Node
    )
async def udpate_node(node_id: int, *, node: schemas.NodeIn):
    # load
    stored_data = crud.get_node(node_id)
    stored_obj = schemas.Node(**stored_data)

    # update
    update_data = node.dict(exclude_unset=True)
    updated_obj = stored_obj.copy(update=update_data)

    # save
    crud.set_node(node_id, jsonable_encoder(updated_obj))

    return node


# DELETE  --------------
# https://cloud.google.com/apis/design/standard_methods#delete
@router.delete("/{node_id}",
    status_code=HTTP_204_NO_CONTENT,
    response_description="Successfully deleted"
    )
async def delete_node(node_id: int):
    print(f"Node {node_id} deleted")

    #If the Delete method immediately removes the resource, it should return an empty response.
    #If the Delete method initiates a long-running operation, it should return the long-running operation.
    #If the Delete method only marks the resource as being deleted, it should return the updated resource.
