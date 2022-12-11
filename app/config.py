import os

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv()


class Settings(BaseSettings):
    MONGODB_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    class Config:
        env_file = os.path.join(os.getcwd(), '.env')


settings = Settings()
