from sqlalchemy import delete, delete, update, update, and_, and_, select, select, insert
from auth.schemas import UserCreate
from .models import User
from auth.utils import get_password_hash
from sqlalchemy.ext.asyncio import session, AsyncSession


async def save_user(user: UserCreate, session: AsyncSession):
    stmt = insert(User).values(
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )
    try:
        await session.execute(stmt)
    except Exception as e:
        print(e)
        raise e
    else:
        await session.commit()


async def get_user_by_username(username: str, session: AsyncSession):
    stmt = select(User).where(User.username==username)
    try:
        data = await session.execute(stmt)
        user = data.fetchone()[0]
    except Exception as e:
        raise e
    else:
        await session.commit()
        return user

async def change_user_password(username: str, password: str,
                               session: AsyncSession):
    stmt = update(User).values(
        hashed_password=get_password_hash(password)
        )
    try:
        await session.execute(stmt)
    except Exception as e:
        raise e
    else:
        await session.commit()


async def delete_user_by_username(username: str, session: AsyncSession):
    stmt = delete(User).where(User.username == username)
    try:
        await session.execute(stmt)
    except Exception as e:
        raise e
    else:
        await session.commit()