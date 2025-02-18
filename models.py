import enum
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True)
    from_questionnaire_id: Mapped[int] = mapped_column(
        ForeignKey('questionnaires.id', ondelete="CASCADE"),
        primary_key=True
    )
    to_questionnaire_id: Mapped[int] = mapped_column(
        ForeignKey('questionnaires.id', ondelete="CASCADE"),
        primary_key=True
    )
    status: Mapped[bool] = mapped_column(default=False)