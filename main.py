import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_tables, delete_tables, async_session, Users
from querries import add_user, add_questionnaire, get_questionnaire, get_feed
from schemas import UserPost, QuestionnairePost, QuestionnaireGet, UserGet, UserGetOne, UserGetForFeed, \
    QuestionnaireGetForFeed

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await delete_tables()
#     print('База очищена')
#     await create_tables()
#     print('База готова к работе')
#     yield
#     print("Выключение")lifespan=lifespan

app = FastAPI()


async def get_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.post('/post-users')
async def add_users(user: Annotated[UserPost, Depends()], session: SessionDep):
    new_user = await add_user(user, session)
    return new_user


@app.post('/post-questionnaire')
async def add_questionnaires(questionnaire: Annotated[QuestionnairePost, Depends()], session: SessionDep):
    new_questionnaire = await add_questionnaire(questionnaire, session)
    return new_questionnaire


@app.get("/get-questionnaires")
async def get_questionnaires(questionnare: Annotated[QuestionnaireGet, Depends()], session: SessionDep):
    questionnaires = await get_questionnaire(user_id=questionnare.user_id, session=session)
    return questionnaires


@app.get("/get-feed")
async def get_feed_func(user: Annotated[UserGetOne, Depends()], session: SessionDep):
    users = await get_feed(user.id, session)
    return users


if __name__ == "__main__":
    uvicorn.run(app)
