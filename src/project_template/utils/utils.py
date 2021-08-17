import base64
import hashlib
import re
from typing import Optional, Tuple

import discord

from project_template import config


# TODO speed this up. Cache the results
def get_tos_version_and_hash(tos: str) -> Tuple[str, str]:
    version = re.findall("^[*]{2}Version[:] ([0-9]{1,10}[.][0-9]{1,10})[*]{2}$", tos, flags=re.M)[0]
    hash_ = hashlib.md5(tos.encode("utf-8")).hexdigest()
    return str(version), hash_


# TODO write test
async def get_bot_message_tos_version_and_hash(
    bot, message_id
) -> Tuple[Optional[str], Optional[str]]:
    if message_id is None:
        return None, None
    channel: discord.TextChannel = bot.get_channel(int(config.DISCORD_TOS_CHANNEL_ID))
    try:
        message_content = (await channel.fetch_message(message_id)).content
        version = re.findall(
            r"^([*]{,2})Version[:]\s*([0-9]{1,10}[.][0-9]{1,10})\1\s*$",
            message_content,
            flags=re.M | re.I,
        )[0][1].strip()
        hash_ = re.findall("TOS Hash[:] (.*)$", message_content, flags=re.M)[0].strip()
    except (discord.errors.NotFound, IndexError):
        return None, None
    return version, hash_


# TODO Cache this.
def get_tos() -> str:
    with open("./PRIVACY.md", "r") as f:
        data = f.read()
    return data


def encode_string_for_db(data: str) -> str:
    return base64.urlsafe_b64encode(data.encode("utf-8")).decode("utf-8")
