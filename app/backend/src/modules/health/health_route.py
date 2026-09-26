from fastapi import APIRouter

health_router = APIRouter(
    prefix = "/health", tags = ["Health"]
)

def hello_world(): 
    print('Hello world') 