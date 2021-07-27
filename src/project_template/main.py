import importlib
import os

from discord.ext import commands

from project_template import config
from project_template.utils.logger import log


bot = commands.Bot(command_prefix=config.DISCORD_BOT_COMMAND_PREFIX)


@bot.event
async def on_ready():
    log.info("Ready")
    # TODO add sending message, version/updates
    pass


@bot.event
async def close():
    # TODO send message on closing
    pass


def gather_cogs():
    def snake_to_camel_case(snake_str):
        components = snake_str.lower().strip().split("_")
        return "".join(x.capitalize() for x in components)

    cogs_list = []
    cogs_to_exclude = set()

    cogs_explicit_exclude = config.COGS_EXPLICIT_EXCLUDE.strip().lower()
    cogs_explicit_include = config.COGS_EXPLICIT_INCLUDE.strip().lower()

    if cogs_explicit_exclude != "":
        cogs_to_exclude = set(cogs_explicit_exclude.split(","))

    if cogs_explicit_include != "":
        for cog_mod in cogs_explicit_include.split(","):
            if cog_mod in cogs_to_exclude:
                continue
            imported_cog = importlib.import_module(f"project_template.cogs.{cog_mod}")
            cogs_list.append(getattr(imported_cog, snake_to_camel_case(cog_mod)))
    else:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        cogs_mods = os.listdir(f"{current_dir}/cogs")
        cogs_mods.remove("__init__.py")
        for cog_mod in cogs_mods:
            if "__" in cog_mod:
                continue
            cog_mod = cog_mod.strip(".py")
            if cog_mod in cogs_to_exclude:
                continue
            imported_cog = importlib.import_module(f"project_template.cogs.{cog_mod}")
            cogs_list.append(getattr(imported_cog, snake_to_camel_case(cog_mod)))

    return cogs_list


if __name__ == "__main__":
    for cog in gather_cogs():
        bot.add_cog(cog(bot))

    bot.run(config.DISCORD_TOKEN)
