from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import db, Token
from app import utils
from app import oauth2


router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)


@router.post("", response_model=Token, status_code=status.HTTP_200_OK, include_in_schema=False)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):

    user = await db["users"].find_one({"username": user_credentials.username})

    if user and utils.verify_password(user_credentials.password, user["password"]):
        access_token = oauth2.create_access_token(payload={
            "id": user["_id"],
        })
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user credentials"
        )
