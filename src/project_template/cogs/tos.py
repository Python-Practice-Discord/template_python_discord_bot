import discord
from discord.ext import commands

from project_template.utils.utils import get_tos, get_tos_version, remove_bot_tos_message
from utils.logger import log
from utils.utils import get_bot_message_id, get_bot_message_tos_version, put_bot_tos_message


class Tos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._tos_message_id = None

    @commands.Cog.listener("on_ready")
    async def get_tos_message_id(self):
        log.info("Getting tos_message_id")

        self._tos_message_id = await get_bot_message_id("project_template_tos")
        message_tos_version = await get_bot_message_tos_version(self.bot, self._tos_message_id)

        tos = get_tos()
        current_tos_version = get_tos_version(tos)

        if message_tos_version != current_tos_version:
            await remove_bot_tos_message(
                self.bot,
                "project_template_tos",
                int(self._tos_message_id)
            )
            self._tos_message_id = None
            # TODO remove users consent when the post is updated. Optional?

        if self._tos_message_id is None:
            self._tos_message_id: int = await put_bot_tos_message(self.bot, "project_template_tos")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        log.info("on reaction add")
        if payload.message_id != self._tos_message_id:
            return

        reaction = payload.emoji.id
        # TODO get tos version
        # TODO make sure it is not a bot reaction

        if reaction == "🟢":
            user_that_reacted = payload.user_id

        elif reaction == "🔴":
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        pass
