import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(os.getenv('DB_LITE_ASYNC'))

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
