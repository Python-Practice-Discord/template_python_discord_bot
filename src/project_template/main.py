import importlib
import os
from typing import List, Set

import discord
from discord.ext import commands

from project_template import config
from project_template.utils.logger import log


bot = commands.Bot(command_prefix=config.DISCORD_BOT_COMMAND_PREFIX)


# TODO add more tests
# TODO clean up utils


@bot.event
async def on_ready():
    log.info("Main on ready start")

    config.DISCORD_TOS_CHANNEL_ID = discord.utils.get(
        bot.get_all_channels(), name=config.config_data["discord"]["tos_channel_name"]
    ).id
    log.debug(f"Set DISCORD_TOS_CHANNEL_ID to {config.DISCORD_TOS_CHANNEL_ID}")

    config.DISCORD_BOT_CHANNEL_ID = discord.utils.get(
        bot.get_all_channels(), name=config.config_data["discord"]["bot_channel_name"]
    ).id
    log.debug(f"Set DISCORD_BOT_CHANNEL_ID to {config.DISCORD_BOT_CHANNEL_ID}")

    message = f"""
{config.BOT_NAME} is starting. Version {config.VERSION}
    """
    channel: discord.TextChannel = bot.get_channel(int(config.DISCORD_BOT_CHANNEL_ID))
    await channel.send(message)


@bot.event
async def close():
    log.info("Main on close")

    message = f"""
{config.BOT_NAME} is shutting down.
        """
    channel: discord.TextChannel = bot.get_channel(int(config.DISCORD_BOT_CHANNEL_ID))
    await channel.send(message)


def gather_cogs():
    def _snake_to_camel_case(snake_str: str) -> str:
        components = snake_str.lower().strip().split("_")
        return "".join(x.capitalize() for x in components)

    def _load_cog(_cogs_list: List, _cog_mod: str, _cogs_to_exclude: Set[str]) -> List:
        if _cog_mod in _cogs_to_exclude:
            log.debug(f"Cog {_cog_mod} being ignored because it is in exclude list")
        else:
            log.info(f"Attempting to load cog {_cog_mod}")
            try:
                imported_cog = importlib.import_module(f"project_template.cogs.{_cog_mod}")
                _cogs_list.append(getattr(imported_cog, _snake_to_camel_case(_cog_mod)))
                log.info(f"Loaded cog {_cog_mod}")
            except ModuleNotFoundError:
                log.exception(f"cog {_cog_mod} not found!")
                raise
        return cogs_list

    log.info("Starting gathering cogs")

    cogs_list = []
    cogs_to_exclude = set()

    cogs_explicit_exclude = config.COGS_EXPLICIT_EXCLUDE.strip().lower()
    cogs_explicit_include = config.COGS_EXPLICIT_INCLUDE.strip().lower()

    log.debug(f"Cogs excluded string {cogs_explicit_exclude}")
    log.debug(f"Cogs included string {cogs_explicit_include}")

    if cogs_explicit_exclude != "":
        cogs_to_exclude = set(cogs_explicit_exclude.split(","))

    if cogs_explicit_include != "":
        log.info("Loading cogs off of include list")
        for cog_mod in cogs_explicit_include.split(","):
            cogs_list = _load_cog(cogs_list, cog_mod, cogs_to_exclude)

    else:
        log.info("Loading cogs dynamically from directory")

        current_dir = os.path.dirname(os.path.realpath(__file__))
        cogs_dir = f"{current_dir}/cogs"
        cogs_mods = os.listdir(cogs_dir)

        log.debug(f"Dir loading cogs from {cogs_dir}")

        for cog_mod in cogs_mods:
            log.info(f"Starting to load cog {cog_mod}")
            if "__" in cog_mod:
                log.debug(f"file {cog_mod} not being loaded because it includes __")
                continue

            cog_mod = cog_mod.strip(".py")
            cogs_list = _load_cog(cogs_list, cog_mod, cogs_to_exclude)

    return cogs_list


if __name__ == "__main__":
    log.info("Running as main")
    for cog in gather_cogs():
        bot.add_cog(cog(bot))

    log.info("About to run bot")
    bot.run(config.DISCORD_TOKEN)
