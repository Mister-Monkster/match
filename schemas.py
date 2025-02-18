from pydantic import BaseModel


class UserPost(BaseModel):
    name: str
    age: int
    gender: str


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


class LikesPost(BaseModel):
    from_questionnaire_id: int
    to_questionnaire_id: int


class SendLike(BaseModel):
    like_id: int
    response: bool






