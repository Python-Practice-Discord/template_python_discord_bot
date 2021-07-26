import base64
import hashlib

from sqlalchemy import select

from project_template import schema
from project_template.config import async_session
from project_template.utils.utils import get_bot_message_id, get_tos_version, put_tos_into_db


async def _test_get_bot_message_id():
    async with async_session() as session:
        async with session.begin():
            session.add(schema.BotMessages(name="test", message_id=100))
            await session.flush()

            message_id = await get_bot_message_id(session=session, message_name="test")

            await session.rollback()
            await session.close()

    assert message_id == 100


def test_get_bot_message_id(main_loop):
    main_loop.run_until_complete(_test_get_bot_message_id())


async def _test_none_bot_message_id():
    message_id = await get_bot_message_id(message_name="test")
    assert message_id is None


def test_none_bot_message_id(main_loop):
    main_loop.run_until_complete(_test_none_bot_message_id())


def test_get_tos_version():
    version = get_tos_version(
        """
**Version: 2.11**
test
    """
    )
    assert version == "2.11"


async def _test_put_tos_into_db_does_not_exist():
    tos = """
**Version: 2.11**
test
    """
    version = get_tos_version(tos)
    async with async_session() as session:
        async with session.begin():
            await put_tos_into_db(session=session, tos=tos, version=version)

            tos_db_hash, tos_db_content = (
                (
                    await session.execute(
                        select(
                            schema.PrivacyTermsOfService.hash,
                            schema.PrivacyTermsOfService.content
                        ).filter(
                            schema.PrivacyTermsOfService.version == version
                        )
                    )
                )
                    .one_or_none()
            )
            await session.rollback()
            await session.close()

    content = base64.urlsafe_b64decode(tos_db_content.encode("utf-8")).decode("utf-8")

    assert tos_db_hash == hashlib.md5(tos.encode("utf-8")).hexdigest()
    assert content == tos


def test_put_tos_into_db_does_not_exist(main_loop):
    main_loop.run_until_complete(_test_put_tos_into_db_does_not_exist())
