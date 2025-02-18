from sqlalchemy import select, and_, update, delete

from models import Users, Questionnaires, Likes
from schemas import UserPost, QuestionnairePost, QuestionnaireGetForFeed, UserGetForFeed, LikesPost, UserGetOne, \
    SendLike


async def get_user(id: int, session):
    query = select(Users).where(Users.id == id)
    res = await session.execute(query)
    res = res.first()
    if res:
        return res[0]
    else:
        return {"message": "no items"}


async def get_questionnaire(user_id: int, session):
    query = select(Questionnaires).where(Questionnaires.user_id == user_id)
    res = await session.execute(query)
    res = res.first()
    if res:
        return res[0]
    else:
        return {"message": "no items"}


async def get_questionnaire_on_id(id: int, session):
    query = select(Questionnaires).where(Questionnaires.id == id)
    res = await session.execute(query)
    res = res.first()
    if res:
        return res[0]
    else:
        return {"message": "no items"}


async def get_like(session, id=None, from_id=None, to_id=None):
    if id:
        query = select(Likes).where(Likes.id == id)
    else:
        query = select(Likes).where(Likes.from_questionnaire_id == from_id, Likes.to_questionnaire_id == to_id)
    like = await session.execute(query)
    res = like.first()
    if res:
        return res[0]
    else:
        return {"message": "no items"}


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
    if not isinstance(questionnaires, dict):
        return {'message': "questionnaire already exist"}
    else:
        questionnaire_dict = questionnaire.model_dump()
        new_questionnaire = Questionnaires(**questionnaire_dict)
        session.add(new_questionnaire)
        await session.commit()
        return {'ok': True}


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
    if users:
        return users
    else:
        return {"meassge": "No items"}


async def update_questionnaires(questionnaire: QuestionnairePost, session):
    query = (update(Questionnaires)
             .where(Questionnaires.user_id == questionnaire.user_id)
             .values(text=questionnaire.text))
    await session.execute(query)
    await session.commit()
    return {'ok': True}


async def send_like(like: LikesPost, session):
    if like.from_questionnaire_id == like.to_questionnaire_id:
        return {'message': "You can't liking yourself"}
    from_obj = await get_questionnaire_on_id(like.from_questionnaire_id, session)
    to_obj = await get_questionnaire_on_id(like.to_questionnaire_id, session)
    to_user = await get_user(to_obj.user_id, session)
    is_like = await get_like(from_id=like.from_questionnaire_id, to_id=like.to_questionnaire_id, session=session)
    if isinstance(is_like, dict):
        query_user = (
            update(Users)
            .where(Users.id == from_obj.user_id)
            .values(activity=to_user.activity + 1)
        )
        query_questionnaire = (
            update(Questionnaires)
            .where(Questionnaires.id == to_obj.id)
            .values(likes=to_obj.likes + 1)
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


async def show_my_likes(user: UserGetOne, session):
    questionnaire = await get_questionnaire(user.id, session)
    query = (select(Likes)
             .where(Likes.to_questionnaire_id == questionnaire.id, Likes.status == False))
    likes = await session.execute(query)
    likes = likes.scalars().all()
    likes_dict = {}
    for like in likes:
        user_questionnaire = await get_questionnaire(like.from_questionnaire_id, session)
        user = await get_user(user_questionnaire.user_id, session)
        likes_dict[f'from_user:{user.id}'] = {"user": {"name": user.name, "age": user.age},
                                              "questionnaire": {"text": user_questionnaire.text}}
    return likes_dict


async def murals_likes(like: SendLike, session):
    got_like = await get_like(session=session, id=like.like_id)
    if like.response:
        got_like.status = True
        response_like = Likes(
            from_questionnaire_id=got_like.to_questionnaire_id,
            to_questionnaire_id=got_like.from_questionnaire_id,
            status=True
        )
        session.add(response_like)
        await session.commit()
        return {"ok": True, "message": "Response successfully sent"}
    else:
        query = delete(Likes).where(Likes.id == got_like.id)
        await session.execute(query)
        await session.commit()
        return {"ok": True, "message": "You're not like this questionnaire"}
