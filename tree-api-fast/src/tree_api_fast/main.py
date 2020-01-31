import uvicorn
from fastapi import FastAPI

from .routers import nodes

app = FastAPI(
    title="Tree API",
    description="Some fast tree API sample",
    version="0.1.4"
)

app.include_router(nodes.router, prefix="/nodes", tags=['nodes'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
