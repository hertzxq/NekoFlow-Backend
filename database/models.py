import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from core.config import DATABASE_URL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
)
logger.info("Database engine created")

Base = declarative_base()


class UsersModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise
