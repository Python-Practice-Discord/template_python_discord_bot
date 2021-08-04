import base64
import datetime
import hashlib
import re
import uuid
from typing import Optional

import arrow
import discord
import sqlalchemy.exc
from sqlalchemy import delete, select

from project_template import config, schema
from project_template.utils.decorators import Session
from project_template.utils.logger import log


@Session
async def get_bot_message_id(session, message_name: str) -> Optional[int]:
    message_id = await session.execute(
        select(
            schema.BotMessages.message_id,
        ).filter(schema.BotMessages.name == message_name)
    )
    message_id = message_id.scalars().one_or_none()
    if message_id is None:
        return message_id
    return int(message_id)


@Session
async def add_user_privacy_tos_agreement(session, discord_id: str, tos_version: str) -> None:
    user_uuid = await get_or_add_user(discord_id)
    user_agreement = schema.UserPrivacyTOS(user_id=user_uuid, tos_version=tos_version)
    try:
        session.add(user_agreement)
        await session.flush()
    except sqlalchemy.exc.IntegrityError:
        log.info("User already agreed to TOS")


async def remove_all_user_data(discord_id: str) -> None:
    await remove_user_privacy_tos_agreement(discord_id)
    await remove_user(discord_id)


@Session
async def remove_user_privacy_tos_agreement(session, discord_id: str) -> None:
    user_id = await get_user_uuid(discord_id=discord_id)
    await session.execute(
        delete(schema.UserPrivacyTOS).where(schema.UserPrivacyTOS.user_id == user_id)
    )


@Session
async def remove_user(session, discord_id: str) -> None:
    await session.execute(delete(schema.User).where(schema.User.discord_id == discord_id))


@Session
async def get_user_uuid(session, discord_id: str) -> Optional[uuid.UUID]:
    user_id: Optional[uuid.UUID] = (
        (await session.execute(select(schema.User.id).filter(schema.User.discord_id == discord_id)))
        .scalars()
        .one_or_none()
    )
    return user_id


@Session
async def get_or_add_user(session, discord_id: str) -> uuid.UUID:
    user_id = await get_user_uuid(discord_id=discord_id)

    if user_id is not None:
        return user_id
    return await add_user(discord_id=discord_id)


@Session
async def add_user(session, discord_id: str) -> uuid.UUID:
    user = schema.User(
        discord_id=discord_id,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    session.add(user)
    await session.flush()
    return user.id


async def get_bot_message_tos_version(bot, message_id) -> Optional[str]:
    if message_id is None:
        return None
    channel: discord.TextChannel = bot.get_channel(int(config.DISCORD_TOS_CHANNEL_ID))
    try:
        message_content = (await channel.fetch_message(message_id)).content
        version = re.findall(
            "TOS Version[:] ([0-9]{1,10}[.][0-9]{1,10})", message_content, flags=re.M
        )[0]
    except (discord.errors.NotFound, IndexError):
        return None
    return version


@Session
async def remove_bot_tos_message(session, bot, message_name: str, message_id: int) -> None:
    channel: discord.TextChannel = bot.get_channel(int(config.DISCORD_TOS_CHANNEL_ID))
    message = await channel.fetch_message(message_id)
    await channel.delete_messages([message])

    await session.execute(delete(schema.BotMessages).where(schema.BotMessages.name == message_name))


@Session
async def put_bot_tos_message(session, bot, message_name: str) -> int:
    tos: str = get_tos()
    version = get_tos_version(tos)
    current_hash = hashlib.md5(tos.encode("utf-8")).hexdigest()

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
    if tos_db_hash is None or current_hash != tos_db_hash:
        await put_tos_into_db(session, tos, version)

    message = f"""
    Privacy Terms of Service of project_template:

    To accept the please react to the 🟢. If you do not want to accept these TOS \
react to the 🔴.

    TOS Link: https://github.com/Python-Practice-Discord/template_python_discord_bot\
/blob/PeterH/expand_package/PRIVACY.md
    TOS Version: {version}
    TOS Hash: {current_hash}
    This post was Updated At: {arrow.utcnow()}
    """
    channel: discord.TextChannel = bot.get_channel(int(config.DISCORD_TOS_CHANNEL_ID))
    sent_message = await channel.send(message)
    session.add(schema.BotMessages(name=message_name, message_id=str(sent_message.id)))
    await session.flush()
    await session.commit()

    await sent_message.add_reaction("🟢")
    await sent_message.add_reaction("🔴")
    return sent_message.id


@Session
async def put_tos_into_db(session, tos: str, version: str) -> None:
    current_hash = hashlib.md5(tos.encode("utf-8")).hexdigest()

    b64_tos = base64.urlsafe_b64encode(tos.encode("utf-8")).decode("utf-8")
    session.add(schema.PrivacyTermsOfService(version=version, content=b64_tos, hash=current_hash))
    await session.flush()


def get_tos() -> str:
    with open("./PRIVACY.md", "r") as f:
        data = f.read()
    return data


def get_tos_version(tos: str) -> str:
    version = re.findall("^[*]{2}Version[:] ([0-9]{1,10}[.][0-9]{1,10})[*]{2}$", tos, flags=re.M)[0]
    return str(version)
