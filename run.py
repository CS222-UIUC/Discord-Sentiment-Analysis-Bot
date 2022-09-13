# run this file when starting up bot
# defines discord bot behavior

import os

import discord
from discord.ext import commands

import config

initial_extensions = ['general']

bot = commands.Bot(command_prefix=config.BOT_PREFIX,
                   pm_help=True, case_insensitive=True)

if __name__ == '__main__':

    config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))

    if config.BOT_TOKEN == "":
        print("Error: No bot token!")
        exit

    for extension in initial_extensions:
        print(f'loading {extension}')
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

@bot.event
async def on_ready():
    print(config.STARTUP_MESSAGE)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="I am Bot, type {}help".format(config.BOT_PREFIX)))

    for guild in bot.guilds:
        print("Joined {}".format(guild.name))

    print(config.STARTUP_COMPLETE_MESSAGE)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    print(message.content)
    # parse message sent here and send to ML model


@bot.event
async def on_guild_join(guild):
    print(guild.name)

bot.run(config.BOT_TOKEN, bot=True, reconnect=True)