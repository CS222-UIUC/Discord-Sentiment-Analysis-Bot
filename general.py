# any defined command is hosted here

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import config

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='ping', description=config.HELP_PING_LONG, help=config.HELP_PING_SHORT)
    async def _ping(self, ctx):
        await ctx.send("Pong")

def setup(bot):
    bot.add_cog(General(bot))