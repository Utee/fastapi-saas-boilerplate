from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Convert postgres:// to postgresql+asyncpg:// needed for Railway compatibility
db_url = settings.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")

engine = create_async_engine(db_url, echo=True, future=True)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session