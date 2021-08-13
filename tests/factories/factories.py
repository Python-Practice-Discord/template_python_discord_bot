import base64
import datetime
import hashlib
import uuid

import arrow
from sqlalchemy.ext.asyncio import AsyncSession

from project_template import schema


async def add_bot_data(session: AsyncSession):
    """
    Adds TOS, bot message, and bot_version
    """
    tos_string = "TEST TOS"
    tos_hash = hashlib.md5(tos_string.encode("utf-8")).hexdigest()
    tos_version = "0.1"

    tos = schema.PrivacyTermsOfService(
        version=tos_version,
        content=base64.urlsafe_b64encode(tos_string.encode("utf-8")).decode("utf-8"),
        hash=tos_hash,
    )
    session.add(tos)

    bot_message = f"""
    TEST

    TOS Version: {tos_version}
    TOS Hash: {tos_hash}
    This post was Updated At: {arrow.utcnow()}
    """

    message = schema.BotMessage(name="project_template_tos", message_id="1234")
    session.add(message)

    bot_version = schema.BotVersion(version="1.0.0", notification_sent=True)
    session.add(bot_version)

    await session.flush()


async def add_user_data(session: AsyncSession) -> uuid.UUID:
    user = schema.User(
        discord_id="1234",
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    session.add(user)
    await session.flush()

    user_privacy_tos = schema.UserPrivacyTOS(user_id=user.id, tos_version="0.1")
    session.add(user_privacy_tos)
    await session.flush()

    return user.id
