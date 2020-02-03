from fastapi import APIRouter

router = APIRouter()


## Standard Methods
# https://cloud.google.com/apis/design/standard_methods


@router.get("/nodes")
async def list_nodes():
    pass

@router.get("/nodes/{node_id}")
async def get_node():
    pass


@router.post("/nodes/{node_id}")
async def create_node():
    pass


@router.patch("/nodes/{node_id}")
async def udpate_node():
    pass


@router.delete("/nodes/{node_id}")
async def delete_node():
    pass
