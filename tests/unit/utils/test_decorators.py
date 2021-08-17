from datetime import datetime

from sqlalchemy import select

from project_template.config import async_session
from project_template.schema import User
from project_template.utils.decorators import Session


@Session
async def add_user_and_confirm(session, clear_session: bool = True):
    new_user = {
        "discord_id": "test_id",
        "created_at": datetime.utcnow(),  # TODO use arrow here
        "updated_at": datetime.utcnow(),
    }
    user = User(**new_user)  # type: ignore
    session.add(user)
    await session.flush()

    statement = select(User).filter_by(discord_id="test_id")
    result = await session.execute(statement)
    result = result.scalars().all()
    if clear_session is True:
        await session.rollback()
        await session.close()
    assert len(result) == 1


async def session_using_dec_session():
    await add_user_and_confirm(clear_session=True)


async def session_using_passed_session():
    statement = select(User).filter_by(discord_id="test_id")

    async with async_session() as session:
        async with session.begin():
            await add_user_and_confirm(session, False)

            result = await session.execute(statement)
            result = result.scalars().all()

            assert len(result) == 1
            await session.rollback()

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(statement)
            result = result.scalars().all()

            assert len(result) == 0


def test_session_using_dec_session(main_loop):
    main_loop.run_until_complete(session_using_dec_session())


def test_session_using_passed_session_2(main_loop):
    main_loop.run_until_complete(session_using_passed_session())
