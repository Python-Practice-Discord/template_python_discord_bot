import arrow
from arrow import ParserError
from discord.ext import commands

from project_template.utils.decorators import TOS
from project_template.utils.logger import log


class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._tos_message_id = None
        self._tos_version = None
        self._tos_hash = None

    @staticmethod
    def _to_upper(timezone: str):
        return timezone.strip().upper()

    @commands.command(name="current_time")
    @TOS(min_tos_version="1.0")
    async def current_time(self, ctx: commands.Context, *, timezone: str):
        log.info(f"Getting current time in timezone: {timezone}")
        tz_converters = [
            None,
            self._to_upper,
        ]
        for tz_converter in tz_converters:
            try:
                if tz_converter is None:
                    timezone = timezone
                else:
                    timezone = tz_converter(timezone)
                time = arrow.utcnow().to(timezone)
                await ctx.send(f"The current time at {timezone} is {time}")
                return
            except ParserError:
                pass
        log.error(f"Could not convert timezone {timezone}")
