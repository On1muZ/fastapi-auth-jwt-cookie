from fastapi import utils, Depends, Request, HTTPException, status
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import decode_JWT
from .schemas import Token
from jwt.exceptions import PyJWKError
from auth.database.utils import get_user_by_username


async def get_current_user(request: Request,
                           session: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            
        )
    cookie = request.cookies.get("access_token")
    try:
        payload = decode_JWT(Token(token=cookie))
        username = payload.username
        if username is None:
            raise credentials_exception
    except:
        raise credentials_exception
    user = await get_user_by_username(username, session)

    if user is None:
        raise credentials_exception

    return user