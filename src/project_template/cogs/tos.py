import discord
from discord.ext import commands

from utils.utils import get_bot_message_id, put_bot_tos_message


class Tos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._tos_message_id = await get_bot_message_id("project_template_tos")

        if self._tos_message_id is None:
            self._tos_message_id: int = await put_bot_tos_message(bot, "project_template_tos")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != self._tos_message_id:
            return

        user_that_reacted = payload.user_id
        reaction = payload.emoji.id
        # TODO get tos version

        if reaction == ":green_circle:":
            pass
        elif reaction == ":red_circle:":
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        pass
