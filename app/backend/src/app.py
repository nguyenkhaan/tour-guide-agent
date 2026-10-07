from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from src.modules.health.health_route import health_router
from sqlalchemy import text
from src.db import engine
from fastapi.middleware.cors import CORSMiddleware
from src.api.settings.config import DATABASE_URL
from src.api.middlewares.request_id_middleware import RequestIDMiddleware
from src.api.https.exception import register_exception_handlers

@asynccontextmanager 
async def lifespan(app : FastAPI): 

    try: 
        async with engine.connect() as engine_connection: 
            await engine_connection.execute(text("SELECT 1"))
        print('Postgres connected') 
    except Exception as e: 
        print(f"Postgres connected failed with: {e}") 
        raise 
    yield

    await engine.dispose() 
    print("Postgres disconnected")


app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:5173" , "https://travel.cloudian.io.vn"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
api_router = APIRouter(
    prefix = "/api"
)

from src.modules.admin.admin_route import admin_router
from src.modules.auth.auth_route import auth_router

api_router.include_router(health_router) 
api_router.include_router(admin_router) 
app.include_router(auth_router)
app.include_router(api_router)
