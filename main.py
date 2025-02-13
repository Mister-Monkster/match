import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from pydantic import BaseModel
from database import create_tables, delete_tables, async_session, Users
from querries import add_user, add_questionnaire, get_questionnaire, get_feed
from schemas import UserPost, QuestionnairePost, QuestionnaireGet, UserGet, UserGetOne

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await delete_tables()
#     print('База очищена')
#     await create_tables()
#     print('База готова к работе')
#     yield
#     print("Выключение")lifespan=lifespan

app = FastAPI()


@app.post('/post-users')
async def add_users(user: Annotated[UserPost, Depends()]):
    await add_user(user)
    return {'ok': True}


@app.post('/post-questionnaire')
async def add_questionnaires(questionnaire: Annotated[QuestionnairePost, Depends()]):
    res = await add_questionnaire(questionnaire)
    return res


@app.get("/get-questionnaires")
async def get_questionnaires(questionnare: Annotated[QuestionnaireGet, Depends()]):
    res = await get_questionnaire(user_id=questionnare.user_id)
    return res


@app.get("/get-feed")
async def get_feed_func(user: Annotated[UserGetOne, Depends()]):
    res = await get_feed(user.id)
    return res

if __name__ == "__main__":
    uvicorn.run(app)
