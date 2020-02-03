
from typing import Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from uuid import UUID



# pagination metadata
class CollectionPage(BaseModel):
    total_size : Optional[int]=0
    next_page_token: str="" # pagination token to retrieve the next page of results. If the value is "", it means no further results for the request.


# shared props
class NodeBase(BaseModel):
    identifier: Optional[UUID]=None
    name: Optional[str] = None


# Properties to receive upon creation
class NodeCreate(NodeBase):
    name: str


# properties to receive on item update
class Node(NodeCreate):
    pass


# Properties to receive upon creation


# Properties to return to client
class NodesList(CollectionPage):
    nodes: List[Node] = []

