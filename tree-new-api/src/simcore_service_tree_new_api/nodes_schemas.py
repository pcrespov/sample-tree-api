
from typing import Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from uuid import UUID



# pagination metadata
class CollectionPage(BaseModel):
    total_size : Optional[int]=0
    next_page_token: str="" # pagination token to retrieve the next page of results. If the value is "", it means no further results for the request.




# Common properties (read/write)
class NodeBase(BaseModel):
    id: UUID
    tag: str

# Properties received to API (read/write)
class NodeIn(NodeBase):
    id: Optional[UUID]=None


# Properties answered in API (read-only)
class Node(NodeBase):
    children_count: int
    depth: int


class NodesList(CollectionPage):
    nodes: List[Node] = []

