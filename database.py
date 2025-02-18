import enum
from typing import Annotated

from sqlalchemy import ForeignKey
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
    name: Mapped[str]
    age: Mapped[int]
    gender: Mapped[Genders]
    questionnaire: Mapped[list["Questionnaires"]] = relationship(back_populates='user')
    activity: Mapped[int] = mapped_column(default=0)


class Questionnaires(Model):
    __tablename__ = "questionnaires"

    id: Mapped[intpk]
    text: Mapped[Annotated[str, 2048]]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    user: Mapped[list["Users"]] = relationship(back_populates='questionnaire')
    likes: Mapped[int] = mapped_column(default=0)


class Likes(Model):
    __tablename__ = 'Likes'

    from_questionnaire_id: Mapped[int] = mapped_column(
        ForeignKey('questionnaires.id', ondelete="CASCADE"),
        primary_key=True
    )
    to_questionnaire_id: Mapped[int] = mapped_column(
        ForeignKey('questionnaires.id', ondelete="CASCADE"),
        primary_key=True
    )
    status: Mapped[bool] = mapped_column(default=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

