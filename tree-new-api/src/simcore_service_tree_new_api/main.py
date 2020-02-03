""" main app

"""
import uvicorn
from fastapi import FastAPI

from . import nodes_routes

app = FastAPI(
    title="Tree API",
    description="An example of RESTful API with a tree abstraction",
    version="0.1.4"
)

# app.include_router(nodes.router, prefix="/trees", tags=['trees'])
# app.include_router(nodes.router, prefix="/trees/{tree_id}/nodes", tags=['nodes'])
app.include_router(nodes_routes.router, prefix="/nodes", tags=['nodes'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
