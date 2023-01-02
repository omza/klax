import jwt

from db.models import User, User_Pydantic
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import config, logging



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')



async def authenticate_user(email: str, password: str):
    user = await User.get(email=email)
    if not user:
        return 
    if not user.verify_password(password):
        return 
    return user 



async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config.SECRET, algorithms=['HS256'])
        id = payload.get('id')
        user = await User.get(id=id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Token is expired'
        )

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    return await User_Pydantic.from_tortoise_orm(user)