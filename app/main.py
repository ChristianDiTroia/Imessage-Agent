from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import HOST_ADDRESS, HOST_PORT
from app.core.logging import logger

app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server at http://{HOST_ADDRESS}:{HOST_PORT}")
    uvicorn.run("app.main:app", host=HOST_ADDRESS, port=HOST_PORT, reload=True)
    logger.info("Server stopped")
