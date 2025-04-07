from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, async_session

from utils.settings import settings


class PostgresSessionFactory:
    def __init__(self):
        self._engine = create_async_engine(url=settings.db.async_dsn, echo=settings.db.show_query)
        self.async_session_maker = async_sessionmaker(self._engine, expire_on_commit=False)
        print(settings.db.async_dsn)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession = self.async_session_maker()
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


session_factory = PostgresSessionFactory()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory.get_session() as session:
        yield session
