from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .routers import strategies, users
from .crud import

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
    version="1.0",
    contact={
        "name": "Lytton Liao",
        "email": "lytton.liao@gmail.com",
    },
)

app.include_router(strategies.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the backend!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
