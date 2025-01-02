from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from models.users import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@database/postgres"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
