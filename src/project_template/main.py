from typing import List

from discord.ext import commands
from project_template import config
from project_template.utils.logger import log


bot = commands.Bot(command_prefix=config.DISCORD_BOT_COMMAND_PREFIX)


@bot.event
async def on_ready(self):
    log.info("Ready")
    # TODO add sending message, version/updates
    pass


@bot.event
async def close(self):
    # TODO send message on closing
    pass


def gather_cogs() -> List[commands.Cog]:
    # This should be set by the settings file
    pass


for cog in gather_cogs():
    bot.add_cog(cog)

bot.run(config.DISCORD_TOKEN)
