import traceback

import discord
from discord.ext import commands

from project_template import config
from project_template.utils.logger import log


def _formatTraceback(tbdat):
    out = ""
    tb = traceback.format_tb(tbdat)
    for part in tb:
        out = out + part + "\n"

    return out


class ErrorHandler(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """A global command error handler."""
        errorName = error.__class__.__name__
        tb = _formatTraceback(error.__traceback__)

        log.error(f"The command {ctx.command} raised and exception: {errorName}")
        channel: discord.TextChannel = discord.utils.get(
            ctx.guild.channels, id=config.DISCORD_ERROR_CHANNEL_ID
        )

        embed = discord.Embed(title="An error has occured!", color=0xFF0000)
        embed.add_field(name="Command", value=ctx.command, inline=True)
        embed.add_field(name="Error", value=errorName, inline=True)
        embed.add_field(name="Traceback", value=f"```{tb}```")

        await channel.send(embed=embed)
