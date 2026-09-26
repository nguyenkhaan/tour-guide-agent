from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from src.modules.health.health_route import health_router
from sqlalchemy import text
from src.db import engine

from src.api.settings.config import DATABASE_URL

# Context manager 
@asynccontextmanager 
async def lifespan(app : FastAPI): 
    # Database checking connection 
    try: 
        async with engine.connect() as engine_connection: 
            await engine_connection.execute(text("SELECT 1"))
        print('Postgres connected') 
    except Exception as e: 
        print(f"Postgres connected failed with: {e}") 
        raise 
    yield
    # closed connection 
    await engine.dispose() 
    print("Postgres disconnected")


app = FastAPI(lifespan=lifespan)

api_router = APIRouter(
    prefix = "/api"
)
api_router.include_router(health_router) 

app.include_router(api_router)