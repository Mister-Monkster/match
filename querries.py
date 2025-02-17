from sqlalchemy import select, and_, update

from database import Users, Questionnaires, Likes
from schemas import UserPost, QuestionnairePost, QuestionnaireGetForFeed, UserGetForFeed, LikesPost


async def get_questionnaire(user_id: int, session):
    query = select(Questionnaires).where(Questionnaires.user_id == user_id)
    res = await session.execute(query)
    res = res.scalars().all()
    return res


async def add_user(user: UserPost, session):
    if user.age <= 110:
        user_dict = user.model_dump()
        new_user = Users(**user_dict)
        session.add(new_user)
        await session.commit()
        return {'ok': True}
    else:
        return {'message': "Please, input correct age"}


async def add_questionnaire(questionnaire: QuestionnairePost, session):
    questionnaires = await get_questionnaire(user_id=questionnaire.user_id, session=session)
    if questionnaires:
        return {'message': "questionnaire already exist"}
    else:
        questionnaire_dict = questionnaire.model_dump()
        new_questionnaire = Questionnaires(**questionnaire_dict)
        session.add(new_questionnaire)
        await session.commit()
        return {'ok': True}


async def get_user(id: int, session):
    query = select(Users).where(Users.id == id)
    res = await session.execute(query)
    return res.scalars().all()


async def get_feed(id: int, session):
    user = await get_user(id, session)
    query = select(Users, Questionnaires).join(Questionnaires).where(and_(Users.age <= user.age + 3,
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


async def update_questionnaires(questionnaire: QuestionnairePost, session):
    query = (update(Questionnaires)
             .where(Questionnaires.user_id == questionnaire.user_id)
             .values(text=questionnaire.text))
    await session.execute(query)
    await session.commit()
    return {'ok': True}


async def get_questionnaire_on_id(id: int, session):
    query = select(Questionnaires).where(Questionnaires.id == id)
    res = await session.execute(query)
    return res.scalars().all()


async def get_like(user_id: int, questionnaire_id: int, session):
    query = select(Likes).where(Likes.user_id == user_id, Likes.questionnaire_id == questionnaire_id)
    like = await session.execute(query)
    return like.scalars().all()


async def send_like(like: LikesPost, session):
    if like.user_id == like.questionnaire_id:
        return {'message': "You can't liking yourself"}
    user_obj = await get_user(like.user_id, session)
    questionnaire_obj = await get_questionnaire_on_id(like.questionnaire_id, session)
    user_obj = user_obj[0]
    questionnaire_obj = questionnaire_obj[0]
    is_like = await get_like(like.user_id, like.questionnaire_id, session)
    if not is_like:
        query_user = (
            update(Users)
            .where(Users.id == user_obj.id)
            .values(activity = user_obj.activity + 1)
        )
        query_questionnaire = (
            update(Questionnaires)
            .where(Questionnaires.id == questionnaire_obj.id)
            .values(likes = questionnaire_obj.likes + 1)
        )
        like_dict = like.model_dump()
        new_like = Likes(**like_dict)
        await session.execute(query_user)
        await session.execute(query_questionnaire)
        session.add(new_like)
        await session.commit()
        return {"ok": True}
    else:
        return {"ok": True, "message": "You already liked this questionnaire"}