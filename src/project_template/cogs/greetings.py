from discord.ext import commands

from project_template.utils.logger import log


# TODO make fake server and try commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        member.send()

    @commands.command()
    async def accept_tos(self, ctx):
        log.info("test")
