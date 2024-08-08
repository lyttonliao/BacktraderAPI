from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routers import strategies
from .utils.errors import register_error_handlers
from .utils.config import app_settings
from .database.session import session_manager


description = """
    Backtrader API allows you to build and test your own trading strategies using an algorithmic testing library, called Backtrader, which was developed by Daniel Rodriguez.

    ## Strategies

    * **Create strategies**
    * **Read strategies**
    * **Update strategies**
    * **Delete strategies**
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
        Function that handles startup and shutdown events
    """

    yield
    if session_manager.engine is not None:
        await session_manager.close()


app = FastAPI(
    title=app_settings.project_name,
    description=description,
    contact={
        "name": "Lytton Liao",
        "email": "lytton.liao@gmail.com",
    },
    debug=app_settings.debug,
    version=str(app_settings.version),
    lifespan=lifespan,
)


app.include_router(strategies.router)

register_error_handlers(app)

origins = app_settings.trusted_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=app,
        host="0.0.0.0", 
        port=8000, 
        reload=True,
    )
