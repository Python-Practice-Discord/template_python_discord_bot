from typing import List

import discord
from discord.ext import commands

from project_template import config
from project_template.utils.database import (
    add_user_privacy_tos_agreement,
    get_bot_message_id,
    put_bot_tos_message,
    remove_all_user_data,
    remove_bot_tos_message,
    remove_non_consenting_users,
)
from project_template.utils.logger import log
from project_template.utils.utils import (
    get_bot_message_tos_version_and_hash,
    get_tos,
    get_tos_version_and_hash,
)
from project_template.utils.decorators import TOS


class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._tos_message_id = None
        self._tos_version = None
        self._tos_hash = None

    @commands.Cog.listener()
    @TOS(min_tos_version="1.0")
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        log.info("TOS on reaction add")
        if payload.message_id != self._tos_message_id or payload.user_id == self.bot.user.id:
            return

        reaction = payload.emoji.name

        if reaction == "🟢":
            user_that_reacted = payload.user_id
            await add_user_privacy_tos_agreement(str(user_that_reacted), self._tos_version)
        elif reaction == "🔴":
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        log.info("TOS on reaction remove")
        if payload.message_id != self._tos_message_id or payload.user_id == self.bot.user.id:
            return

        reaction = payload.emoji.name

        if reaction == "🟢":
            user_that_reacted = payload.user_id
            await remove_all_user_data(str(user_that_reacted))
        elif reaction == "🔴":
            return


@TOS(min_tos_version="1.0")
def something_test():
    return True

if __name__ == '__main__':
    print(something_test())
