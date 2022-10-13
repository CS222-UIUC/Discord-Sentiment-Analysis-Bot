import pytest
import discord.ext.test as dpytest
from discord.ext import commands
from discord import Intents

@pytest.mark.asyncio
async def test_bot():
    bot = commands.Bot("/", intents=Intents(members=True))

    @bot.command()
    async def ping(ctx):
        await ctx.send("pong")

    dpytest.configure(bot)

    await dpytest.message("/ping")
    assert dpytest.verify().message().content("pong")