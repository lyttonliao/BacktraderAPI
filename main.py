from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .routers import strategies, users
from utils.errors import register_error_handlers

description = """
    Backtrader API allows you to build and test your own trading strategies using an algorithmic testing library, called Backtrader, which was developed by Daniel Rodriguez.

    ## Strategies

    * **Create strategies**
    * **Read strategies**
    * **Update strategies**
    * **Delete strategies**
"""

app = FastAPI(
    title="BacktraderAPI",
    description=description,
    version=1,
    contact={
        "name": "Lytton Liao",
        "email": "lytton.liao@gmail.com",
    },
)

app.include_router(strategies.router)

register_error_handlers(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
