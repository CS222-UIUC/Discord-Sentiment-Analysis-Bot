# bot.py
import os
import config
import discord

bot = discord.Client()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await message.channel.send("pong")

bot.run(config.BOT_TOKEN)