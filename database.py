import enum
from typing import Optional, Annotated

from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_async_engine(
    url="postgresql+asyncpg://postgres:1@localhost:5432/firstApp"
)

async_session = async_sessionmaker(engine, expire_on_commit=False)
intpk = Annotated[int, mapped_column(primary_key=True)]


class Model(DeclarativeBase):
    pass


class Genders(enum.Enum):
    male = 'male'
    female = 'female'


class Users(Model):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str]
    name: Mapped[str]
    age: Mapped[int]
    gender: Mapped[Genders]
    # questionnaires_id: Mapped[int] = mapped_column(ForeignKey('questionnaires.id', ondelete="CASCADE"))
    questionnaire: Mapped[list["Questionnaires"]] = relationship(back_populates='user')


class Questionnaires(Model):
    __tablename__ = "questionnaires"

    id: Mapped[intpk]
    text: Mapped[Annotated[str, 2048]]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    user: Mapped[list["Users"]] = relationship(back_populates='questionnaire')


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

