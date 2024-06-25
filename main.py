from fastapi import FastAPI
from .routers import strategies

app = FastAPI()

app.include_router(strategies.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the backend!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
