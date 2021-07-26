import base64
import hashlib
import re
from typing import Optional

import discord
from sqlalchemy import select

import config
from project_template import schema
from project_template.utils.decorators import Session


@Session
async def get_bot_message_id(session, message_name: str) -> Optional[int]:
    message_id = await session.execute(
        select(schema.BotMessages.message_id).filter(schema.BotMessages.name == message_name)
    )
    message_id = message_id.scalars().one_or_none()
    return message_id


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

    To accept the please react to the :green_circle:. If you do not want to accept these TOS react to the :red_circle:.

    TOS Link: https://github.com/Python-Practice-Discord/template_python_discord_bot/blob/PeterH/expand_package/PRIVACY.md
    TOS Hash: {current_hash}
    """
    channel: discord.TextChannel = bot.get_channel(config.DISCORD_TOS_CHANNEL_ID)
    sent_message = await channel.send(message)
    await sent_message.add_reaction(":green_circle")
    await sent_message.add_reaction(":red_circle")

    session.add(
        schema.BotMessages(name=message_name, message_id=sent_message.id)
    )
    await session.flush()

    return sent_message.id


@Session
async def put_tos_into_db(session, tos: str, version: str) -> None:
    current_hash = hashlib.md5(tos.encode("utf-8")).hexdigest()

    b64_tos = base64.urlsafe_b64encode(tos.encode("utf-8")).decode("utf-8")
    session.add(
        schema.PrivacyTermsOfService(version=version, content=b64_tos, hash=current_hash)
    )
    await session.flush()


def get_tos() -> str:
    with open("./PRIVACY.md", "r") as f:
        data = f.read()
    return data


def get_tos_version(tos: str) -> str:
    version = re.findall("^[*]{2}Version[:] ([0-9]{1,10}[.][0-9]{1,10})[*]{2}$", tos, flags=re.M)[0]
    return str(version)
