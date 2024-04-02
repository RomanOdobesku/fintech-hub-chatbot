import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


print(os.getenv('DB_POSTGRESQL_ASYNC'))
engine = create_async_engine(os.getenv('DB_POSTGRESQL_ASYNC'))

session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
