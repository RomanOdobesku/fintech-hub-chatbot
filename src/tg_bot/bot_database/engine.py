from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# engine = create_async_engine(os.getenv('DB_POSTGRESQL_ASYNC'))

connection_string = URL.create(
  'postgresql+asyncpg',
  username='olga',
  password='XGAs4trRJ0hW',
  host='ep-bold-mouse-a2jqmrzs.eu-central-1.aws.neon.tech',
  database='postgresql',
  query={'ssl': 'require'}
)

engine = create_async_engine(connection_string, echo=True)

session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
