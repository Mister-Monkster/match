from sqlalchemy import select, and_

from database import async_session, Users, Questionnaires
from schemas import UserPost, QuestionnairePost, QuestionnaireGet, UserGet, QuestionnaireGetForFeed, UserGetForFeed


async def get_questionnaire(user_id: int):
    async with async_session.begin() as session:
        query = select(Questionnaires).filter(Questionnaires.user_id == user_id)
        res = await session.execute(query)
        result = res.scalars().all()
        return result


async def add_user(user: UserPost):
    async with async_session.begin() as session:
        new_user = Users(
            username=user.username,
            name=user.name,
            age=user.age,
            gender=user.gender
        )
        session.add(new_user)
        session.commit()


async def add_questionnaire(questionnaire: QuestionnairePost):
    questionnaires = await get_questionnaire(user_id=questionnaire.user_id)
    if questionnaires:
        return {"ok": True, "message": "questionnaire already exist"}
    else:
        async with async_session.begin() as session:
            new_questionnaire = Questionnaires(
                text = questionnaire.text,
                user_id = questionnaire.user_id
            )
            session.add(new_questionnaire)
            session.commit()
            return {"ok": True}


async def get_user(id: int):
    async with async_session.begin() as session:
        query = select(Users).filter(Users.id == id)
        res = await session.execute(query)
        return res.scalars().one()


async def get_feed(id: int):
    async with async_session.begin() as session:
        user = await get_user(id)
        query = select(Users, Questionnaires).join(Questionnaires).filter(and_(Users.age <= user.age + 3,
                                                   Users.age >= user.age - 3,
                                                   Users.gender != user.gender))
        res = await session.execute(query)
        users = {}

        for us, qst in res.all():
            result1 = UserGetForFeed(
                name=us.name,
                age=us.age,
                gender=us.gender
            )

            result2 = QuestionnaireGetForFeed(
                text=qst.text
            )

            users[f'{us.id=}'] = {"user": result1, "questionnairie": result2}
        return users
