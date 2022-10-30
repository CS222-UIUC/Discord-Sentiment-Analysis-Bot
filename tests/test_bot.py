"""Testing framework for testing the bot"""
import pytest
import discord.ext.test as dpytest
from discord.ext import commands
from discord import Intents

import sys
sys.path.append('../COURSE-PROJECT-GROUP-38')

# import discord_bot.bot as dbot

@pytest.mark.asyncio
async def test_bot():
    """
        description: test cases are writted here for the bot
    """
    import discord_bot.bot as dbot

    dpytest.configure(dbot.bot)

    await dpytest.message("-ping")
    assert dpytest.verify().message().content("pong")