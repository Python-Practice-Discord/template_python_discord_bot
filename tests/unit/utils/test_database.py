import base64
import hashlib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from project_template import schema
from project_template.config import async_session
from project_template.utils.database import (
    get_bot_message_id,
    put_tos_into_db,
    remove_non_consenting_users,
)
from project_template.utils.utils import get_tos_version_and_hash
from tests.factories.factories import add_bot_data, add_user_data


# TODO test deleting all data from DB.


# get_bot_message_id
async def _test_get_bot_message_id():
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            session.add(schema.BotMessage(name="test", message_id="100"))
            await session.flush()

            message_id = await get_bot_message_id(session=session, message_name="test")

            await session.rollback()
            await session.close()

    assert message_id == 100


def test_get_bot_message_id(main_loop):
    main_loop.run_until_complete(_test_get_bot_message_id())


async def _test_get_bot_message_id_none():
    message_id = await get_bot_message_id(message_name="test")
    assert message_id is None


def test_get_bot_message_id_none(main_loop):
    main_loop.run_until_complete(_test_get_bot_message_id_none())


# remove_non_consenting_users
async def _test_remove_non_consenting_users():
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            await add_bot_data(session)
            user_id = await add_user_data(session)
            await remove_non_consenting_users(session, ["1234"])
            await session.flush()
            user = (
                await session.execute(select(schema.User).filter(schema.User.id == user_id))
            ).one()[0]
            assert user.id == user_id

            await remove_non_consenting_users(session, ["fake_id"])
            await session.flush()
            user = (
                await session.execute(select(schema.User).filter(schema.User.id == user_id))
            ).one_or_none()
            assert user is None

            await session.rollback()
            await session.close()


def test_remove_non_consenting_users(main_loop):
    main_loop.run_until_complete(_test_remove_non_consenting_users())


async def _test_put_tos_into_db_does_not_exist():
    tos = """
**Version: 2.11**
test
    """
    version, hash_ = get_tos_version_and_hash(tos)
    async with async_session() as session:
        async with session.begin():
            await put_tos_into_db(session=session, tos=tos, version=version, hash_=hash_)

            tos_db_hash, tos_db_content = (
                await session.execute(
                    select(
                        schema.PrivacyTermsOfService.hash, schema.PrivacyTermsOfService.content
                    ).filter(schema.PrivacyTermsOfService.version == version)
                )
            ).one_or_none()
            await session.rollback()
            await session.close()

    content = base64.urlsafe_b64decode(tos_db_content.encode("utf-8")).decode("utf-8")

    assert tos_db_hash == hashlib.md5(tos.encode("utf-8")).hexdigest()
    assert content == tos


def test_put_tos_into_db_does_not_exist(main_loop):
    main_loop.run_until_complete(_test_put_tos_into_db_does_not_exist())
