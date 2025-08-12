from fastapi import FastAPI
from order_routes import order_router
from auth_routes import auth_router
from fastapi_jwt_auth import AuthJWT
from database import Base, engine
from schemas import Settings
from models import Base

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

@app.get("/")
def root():
    return {"message": "Welcome to the Pizza API"}

app.include_router(order_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)