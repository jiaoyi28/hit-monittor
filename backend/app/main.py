from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.repositories import router as repositories_router
from app.api.routes.settings import router as settings_router
from app.core.database import initialize_database


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    initialize_database()
    yield


app = FastAPI(title="hit-monittor", lifespan=lifespan)

app.include_router(dashboard_router)
app.include_router(repositories_router)
app.include_router(settings_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
