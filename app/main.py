from fastapi import FastAPI

from app.routes import auth
from app.routes import password
from app.routes import users


app = FastAPI(title="Yakut-API")


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(password.router)