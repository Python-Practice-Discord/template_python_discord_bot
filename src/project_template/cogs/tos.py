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


class Tos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._tos_message_id = None
        self._tos_version = None
        self._tos_hash = None

    @commands.Cog.listener("on_ready")
    async def get_tos_message_id(self):
        # WARNING! when the TOS version is changed all user data WILL BE DELETED!
        log.info("Getting tos_message_id")

        self._tos_message_id = await get_bot_message_id("project_template_tos")
        message_tos_version, message_tos_hash = await get_bot_message_tos_version_and_hash(
            self.bot, self._tos_message_id
        )

        tos = get_tos()
        self._tos_version, self._tos_hash = get_tos_version_and_hash(tos)

        if message_tos_hash != self._tos_hash and self._tos_message_id is not None:
            await remove_bot_tos_message(
                self.bot, "project_template_tos", int(self._tos_message_id)
            )
            self._tos_message_id = None

        if self._tos_message_id is None:
            self._tos_message_id: int = await put_bot_tos_message(self.bot, "project_template_tos")

        await self._sync_reactions()

    async def _sync_reactions(self):
        """
        Makes sure all reactions since the bot was last turned on have been synced.
        """
        # TODO remove users who removed their consent.

        channel: discord.TextChannel = self.bot.get_channel(int(config.DISCORD_TOS_CHANNEL_ID))
        message = await channel.fetch_message(self._tos_message_id)
        reactions = message.reactions

        current_consent_discord_ids: List[str] = []
        for reaction in reactions:
            if reaction.emoji != "🟢":
                continue
            async for user in reaction.users():
                if user.id == self.bot.user.id:
                    continue
                await add_user_privacy_tos_agreement(str(user.id), self._tos_version)
                current_consent_discord_ids.append(str(user.id))
        await remove_non_consenting_users(current_consent_discord_ids)

    @commands.Cog.listener()
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
