"""any defined command is hosted here"""

import discord #pylint: disable=W0611
from discord.ext import commands
from discord.ext.commands import has_permissions #pylint: disable=W0611

import discord_bot.config as config #pylint: disable=E0401 #pylint: disable=R0402

class General(commands.Cog):
    """Class with commands for bot"""
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='ping', description=config.HELP_PING_LONG, help=config.HELP_PING_SHORT)
    async def _ping(self, ctx):
        await ctx.send("Pong")

def setup(bot):
    """"Function to setup bot"""
    bot.add_cog(General(bot))
