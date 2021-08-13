import base64
import datetime
import uuid
from typing import List, Optional

import arrow
import discord
import sqlalchemy.exc
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from project_template import config, schema
from project_template.utils.decorators import Session
from project_template.utils.logger import log
from project_template.utils.utils import get_tos, get_tos_version_and_hash


@Session
async def get_bot_message_id(session: AsyncSession, message_name: str) -> Optional[int]:
    message_id = (
        (
            await session.execute(
                select(
                    schema.BotMessage.message_id,
                ).filter(schema.BotMessage.name == message_name)
            )
        )
        .scalars()
        .one_or_none()
    )
    if message_id is None:
        return message_id
    return int(message_id)


@Session
async def remove_non_consenting_users(
    session: AsyncSession, current_consent_discord_ids: List[str]
):
    discord_ids = (await session.execute(select(schema.User.discord_id))).scalars()
    for user_id in discord_ids:
        if str(user_id) not in current_consent_discord_ids:
            await remove_all_user_data(session, user_id)


@Session
async def add_user_privacy_tos_agreement(
    session: AsyncSession, discord_id: str, tos_version: str
) -> None:
    user_uuid = await get_or_add_user(session, discord_id)
    user_agreement = schema.UserPrivacyTOS(user_id=user_uuid, tos_version=tos_version)
    try:
        session.add(user_agreement)
        await session.flush()
    except sqlalchemy.exc.IntegrityError:
        log.info("User already agreed to TOS")


@Session
async def remove_all_user_data(session: AsyncSession, discord_id: str) -> None:
    await remove_user_privacy_tos_agreement(session=session, discord_id=discord_id)
    await remove_user(session=session, discord_id=discord_id)


async def remove_user_privacy_tos_agreement(session: AsyncSession, discord_id: str) -> None:
    user_id = await get_user_uuid(session=session, discord_id=discord_id)
    await session.execute(
        delete(schema.UserPrivacyTOS).where(schema.UserPrivacyTOS.user_id == user_id)
    )
    await session.flush()


async def remove_user(session: AsyncSession, discord_id: str) -> None:
    await session.execute(delete(schema.User).where(schema.User.discord_id == discord_id))
    await session.flush()


async def get_user_uuid(session: AsyncSession, discord_id: str) -> Optional[uuid.UUID]:
    user_id: Optional[uuid.UUID] = (
        (await session.execute(select(schema.User.id).filter(schema.User.discord_id == discord_id)))
        .scalars()
        .one_or_none()
    )
    return user_id


async def get_or_add_user(session, discord_id: str) -> uuid.UUID:
    user_id = await get_user_uuid(session=session, discord_id=discord_id)

    if user_id is not None:
        return user_id
    return await add_user(session=session, discord_id=discord_id)


async def add_user(session: AsyncSession, discord_id: str) -> uuid.UUID:
    user = schema.User(
        discord_id=discord_id,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    session.add(user)
    await session.flush()
    return user.id


@Session
async def remove_bot_tos_message(
    session: AsyncSession, bot, message_name: str, message_id: int
) -> None:
    channel: discord.TextChannel = bot.get_channel(int(config.DISCORD_TOS_CHANNEL_ID))
    message = await channel.fetch_message(message_id)
    await channel.delete_messages([message])

    await session.execute(delete(schema.BotMessage).where(schema.BotMessage.name == message_name))


@Session
async def put_bot_tos_message(session: AsyncSession, bot, message_name: str) -> int:
    tos: str = get_tos()
    version, hash_ = get_tos_version_and_hash(tos)

    tos_db_hash = (
        (
            await session.execute(
                select(schema.PrivacyTermsOfService.hash).filter(
                    schema.PrivacyTermsOfService.version == version
                )
            )
        )
        .scalars()
        .one_or_none()
    )
    # TODO do we want this to fail if something is changed but the version is not bumped?
    # TODO if a version is changed ALL USER DATA WILL BE DELETED! Do we want this?
    if tos_db_hash is None or hash_ != tos_db_hash:
        await put_tos_into_db(session, tos, version, hash_)

    message = f"""
    Privacy Terms of Service of project_template:

    To accept the please react to the 🟢. If you do not want to accept these TOS \
react to the 🔴.

    TOS Link: https://github.com/Python-Practice-Discord/template_python_discord_bot\
/blob/PeterH/expand_package/PRIVACY.md
    TOS Version: {version}
    TOS Hash: {hash_}
    This post was Updated At: {arrow.utcnow()}
    """
    channel: discord.TextChannel = bot.get_channel(int(config.DISCORD_TOS_CHANNEL_ID))
    sent_message = await channel.send(message)
    session.add(schema.BotMessage(name=message_name, message_id=str(sent_message.id)))
    await session.flush()
    await session.commit()

    await sent_message.add_reaction("🟢")
    await sent_message.add_reaction("🔴")
    return sent_message.id


async def put_tos_into_db(session: AsyncSession, tos: str, version: str, hash_: str) -> None:
    b64_tos = base64.urlsafe_b64encode(tos.encode("utf-8")).decode("utf-8")
    session.add(schema.PrivacyTermsOfService(version=version, content=b64_tos, hash=hash_))
    await session.flush()
