from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import HOST_PORT

app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=HOST_PORT, reload=True)
