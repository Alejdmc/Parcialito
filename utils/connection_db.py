from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from sqlmodel import SQLModel


CLEVER_DB = (
    "postgresql+asyncpg://uxvzn3b7cgwi95jff61f:HH11sQzeFmenVZ5fMdOgT5blLISQwu@"
    "bsgpdihy3vwaex0141iw-postgresql.services.clever-cloud.com:50013/bsgpdihy3vwaex0141iw"
)

engine = create_async_engine(CLEVER_DB,echo=True)


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

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
async def agregar_columna():
    engine = create_async_engine(CLEVER_DB)
    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE artistadb ADD COLUMN IF NOT EXISTS id int"))
        await conn.execute(text("ALTER TABLE Mascotas ADD COLUMN id VARCHAR;"))
        await conn.execute(text("ALTER TABLE Vuelos ADD COLUMN id VARCHAR;"))
        await conn.execute(text("ALTER TABLE Usuarios ADD COLUMN id VARCHAR;"))
    await engine.dispose()

if __name__ == "__main__":
    import asyncio
    asyncio.run(agregar_columna())
async def close_db_connections():
    await engine.dispose()
