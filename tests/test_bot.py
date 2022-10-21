"""Testing framework for testing the bot"""
from discord_bot.config import BOT_PREFIX
import pytest
import discord.ext.test as dpytest
from discord.ext import commands
from discord import Intents
from discord_bot import config

@pytest.mark.asyncio
async def test_bot():
    """
        message: test cases are writted here for the bot
    """
    bot = commands.Bot("/", intents=Intents().all())

    @bot.command()
    async def ping(ctx):
        await ctx.send("pong")

    dpytest.configure(bot)

    await dpytest.message("/ping")
    assert dpytest.verify().message().content("pong")

def test_config():
    assert config.BOT_PREFIX == "-"

    assert config.STARTUP_MESSAGE == "Starting Bot..."
    assert config.STARTUP_COMPLETE_MESSAGE == "Startup Complete"

    assert config.HELP_PING_SHORT == "Pong"
    assert config.HELP_PING_LONG == "Test bot response status"