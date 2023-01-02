import jwt

from fastapi import APIRouter, Depends
from db.models import User, User_Pydantic, UserIn_Pydantic
from dependencies import get_current_user
from config import config, logging

from passlib.hash import bcrypt

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

 
@router.post('/', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(
        firstname = user.firstname,
        email=user.email, 
        password_hash=bcrypt.hash(user.password_hash),
        admin_role = 0,
        active = 0
    )
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@router.get('/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user   