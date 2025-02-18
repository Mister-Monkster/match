from typing import Annotated

from fastapi import FastAPI, Depends
import uvicorn

from sqlalchemy.ext.asyncio import AsyncSession

from database import create_tables, delete_tables, async_session
from querries import add_user, add_questionnaire, get_questionnaire, get_feed, update_questionnaires, send_like, \
    show_my_likes
from schemas import UserPost, QuestionnairePost, QuestionnaireGet, UserGetOne, LikesPost

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

tags = ["Match"]

@app.post('/post-users',
          summary='Добавить пользователя',
          tags=tags)
async def add_users(user: Annotated[UserPost, Depends()], session: SessionDep):
    new_user = await add_user(user, session)
    return new_user


@app.post('/post-questionnaire',
          summary='Добавить анкету',
          tags=tags)
async def add_questionnaires(questionnaire: Annotated[QuestionnairePost, Depends()], session: SessionDep):
    new_questionnaire = await add_questionnaire(questionnaire, session)
    return new_questionnaire

@app.post('/update-questionnaire',
          summary='Обновить анкету',
          tags=tags)
async def update_questionnaire(questionnaire: Annotated[QuestionnairePost, Depends()], session: SessionDep):
    return await update_questionnaires(questionnaire, session)


@app.get("/get-questionnaires",
         summary='Получить анкету',
          tags=tags)
async def get_questionnaires(questionnare: Annotated[QuestionnaireGet, Depends()], session: SessionDep):
    questionnaires = await get_questionnaire(user_id=questionnare.user_id, session=session)
    return questionnaires


@app.get(path="/get-feed",
         summary='Лента',
          tags=tags)
async def get_feed_func(user: Annotated[UserGetOne, Depends()], session: SessionDep):
    users = await get_feed(user.id, session)
    return users


@app.post(path='/send-likes',
          summary='Поставить лайк👍',
          tags=tags)
async def send_likes(like: Annotated[LikesPost, Depends()],
                     session: SessionDep):
    like = await send_like(like, session)
    return like


@app.get(path='/my-likes',
         summary='Получить мои лайки👍',
         tags=tags)
async def get_my_likes(user: Annotated[UserGetOne, Depends()], session: SessionDep):
    res = await show_my_likes(user, session)
    return res


if __name__ == "__main__":
    uvicorn.run(app)
