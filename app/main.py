from fastapi import FastAPI

from app.routes import auth
from app.routes import password
from app.routes import users

from app.config import settings

app = FastAPI(title="Yakut-API")


print(settings)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(password.router)