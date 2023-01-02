import jwt

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm

from db.models import User_Pydantic, UserIn_Pydantic
from dependencies import authenticate_user, get_current_user
from config import config, logging

from datetime import datetime, timezone, timedelta

router = APIRouter(
    prefix="/token",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

response_unauthorized = {"401": {
            "detail": "Validation Error",
    }
}

@router.post('/', status_code=status.HTTP_201_CREATED)
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    user_obj = await User_Pydantic.from_tortoise_orm(user)
    valid_until = datetime.now(tz=timezone.utc) + timedelta(seconds=30)

    token = jwt.encode(
        {
            "id" : user_obj.id,
            "exp": valid_until
        }, 
        config.SECRET)

    return {'access_token' : token, 'token_type' : 'bearer', 'valid_until': valid_until} #, "valid_until": valid_until

@router.get('/refresh', status_code=status.HTTP_201_CREATED, responses=response_unauthorized)
async def refresh_token(user: User_Pydantic = Depends(get_current_user)):

    valid_until = datetime.now(tz=timezone.utc) + timedelta(seconds=30)

    token = jwt.encode(
        {
            "id" : user.id,
            "exp": valid_until
        }, 
        config.SECRET)

    return {'access_token' : token, 'token_type' : 'bearer', "valid_until": valid_until}