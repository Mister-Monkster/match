from typing import Optional

from pydantic import BaseModel


class UserPost(BaseModel):
    name: str
    age: int
    gender: str


class UserGet(UserPost):
    id: int


class UserGetOne(BaseModel):
    id: int


class UserGetForFeed(BaseModel):
    name: str
    age: int
    gender: str


class QuestionnaireGet(BaseModel):
    user_id: int


class QuestionnairePost(QuestionnaireGet):
    text: str


class QuestionnaireGetForFeed(BaseModel):
    text: str






