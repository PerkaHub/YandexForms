from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.handlers import setup_exception_handlers

app = FastAPI()

app.include_router(auth_router)

setup_exception_handlers(app)
