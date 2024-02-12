from fastapi import responses, APIRouter, Depends, Response, HTTPException, status
from .schemas import UserCreate, BaseUser, UserPasswordChange, UserPassword
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .database.utils import save_user, get_user_by_username, change_user_password, delete_user_by_username
from .database.models import User
from .utils import verify_password, sign_JWT
from .dependencies import get_current_user


router = APIRouter(prefix="/api/auth/jwt")


@router.post("/signup")
async def sign_up_user(user: UserCreate,
                       session: AsyncSession = Depends(get_async_session)):
    try:
        await save_user(user, session)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="This username has already taken. Try another one")
    else:
        raise HTTPException(status_code=status.HTTP_201_CREATED)


@router.post("/signin")
async def sign_in_user(user: UserCreate,
                       response: Response,
                       session: AsyncSession = Depends(get_async_session)):
    try:
        user_from_db = await get_user_by_username(user.username, session)
        if user_from_db is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password")
        elif not verify_password(user.password, user_from_db.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password")
        else:
            token = sign_JWT(BaseUser(user_id=user_from_db.id,
                            username=user_from_db.username))
            response.set_cookie(key="access_token",value=token.token, httponly=True)
            return {
                "id": user_from_db.id,
                "username": user_from_db.username
            }
    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect username or password")


@router.get('/me')
async def get_me(user = Depends(get_current_user)) -> BaseUser:
    return BaseUser(
        user_id=user.id,
        username=user.username
    )


@router.get('/logout')
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {
        "status": 200
    }


@router.patch("/change_password")
async def change_password(user_password: UserPasswordChange,
                          user: User = Depends(get_current_user),
                          session: AsyncSession = Depends(get_async_session)):
    if not verify_password(user_password.password,
                           user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        await change_user_password(
            user.username,
            user_password.new_password,
            session
        )
        raise HTTPException(status_code=status.HTTP_200_OK)


@router.delete("/delete")
async def delete_user(user_password: UserPassword,
                      response: Response,
                      user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_async_session)):
    if not verify_password(user_password.password,
                           user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        await delete_user_by_username(user.username, session)
        response.delete_cookie("access_token")
        return {
            "status": 200
        }