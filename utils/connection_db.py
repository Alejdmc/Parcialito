from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from sqlmodel import SQLModel


CLEVER_DB = (
    "postgresql+asyncpg://uopben1tyj1wczzghysd:2qME5NqVJBqOwHSG1qqeYqbtj7mW8X@"
    "bcyupf1pgnbj04g0dfnv-postgresql.services.clever-cloud.com:50013/bcyupf1pgnbj04g0dfnv"
)
engine = create_async_engine(
    CLEVER_DB,
    echo=False,
    pool_size=5,
    max_overflow=0,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=60,
    poolclass=AsyncAdaptedQueuePool
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db_connections():
    await engine.dispose()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session