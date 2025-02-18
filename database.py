from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine(
    url="postgresql+asyncpg://postgres:1@localhost:5432/firstApp"
)

async_session = async_sessionmaker(engine, expire_on_commit=False)




