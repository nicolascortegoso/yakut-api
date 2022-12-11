from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app import oauth2
from app.schemas import User, UserResponse, db
from app.utils import get_password_hash
from app.send_email import send_registration_mail
import secrets


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/registration",
             response_description="Register New User",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
async def registration(user_info: User):
    user_info = jsonable_encoder(user_info)

    username_found = await db["users"].find_one({"username": user_info["username"]})
    email_found = await db["users"].find_one({"email": user_info["email"]})

    if username_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="There already is a user by that username")

    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="There already is a user by that email")

    user_info["password"] = get_password_hash(user_info["password"])
    user_info["apiKey"] = secrets.token_hex(20)
    new_user = await db["users"].insert_one(user_info)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})

    await send_registration_mail("Registration successful", user_info["email"],
        {
            "title": "Registration successful",
            "username": user_info["username"]
        }
    )

    return created_user


@router.post("/me", response_description="Get user details", response_model=UserResponse)
async def details(current_user=Depends(oauth2.get_current_user)):
    user = await db["users"].find_one({"_id": current_user["_id"]})
    return user
