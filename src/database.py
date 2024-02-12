from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import Settings


settings = Settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.pg_database.user}:{settings.pg_database.password}@{settings.pg_database.host}:{settings.pg_database.port}/{settings.pg_database.name}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session