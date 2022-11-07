"""Testing framework for testing the bot"""
import pytest
import discord.ext.test as dpytest
from discord.ext import commands
from discord import Intents
import random

@pytest.mark.asyncio
async def test_basic():
    """
        description: test cases are writted here for the bot
    """
    # pylint: disable=C0415
    bot = commands.Bot("-", intents=Intents().all())

    @bot.command()
    async def ping(ctx):
        """
        generic test function
        """
        await ctx.send("pong")

    dpytest.configure(bot)

    await dpytest.message("-ping")
    assert dpytest.verify().message().content("pong")

@pytest.mark.asyncio
async def test_reaction():
    """
        description: test cases are writted here for the bot
    """
    bot = commands.Bot("-", intents=Intents().all())
    def determine_sentiment(message):
            """
            Arguments:
                message: message content from discord message
            Returns:
                sentiment -1, 0, 1
            """
            print(message)
            # simulate positive connotation for test case
            return 1

    @bot.command()
    async def verify(ctx):
        """
        brains of the discord bot
        Arguments:
            message: message from discord picked up by API
        Returns:
            will react according to messages sent by user. defined below
        """

        sentiment = determine_sentiment(ctx.message.content)
        print("sentiment", sentiment) # for debugging purposes

        if sentiment == 1:
            await ctx.send('👍')

        elif sentiment == 0:
            await ctx.send('👊')

        else: # sentiment == -1
            await ctx.send('👎')

    dpytest.configure(bot)
    # await verify("-verify this is a positive test message!")
    await dpytest.message("-verify this is a positive test message!")
    # res1 =  dpytest.verify().message().content('👍')
    assert dpytest.verify().message().content('👍')
