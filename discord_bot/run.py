"""Module used to run the discord bot"""

import discord
import discord_bot.config as config #pylint: disable=E, R0402

intents = discord.Intents.default()

class MyClient(discord.Client):
    """Discord bot client class"""
    async def on_ready(self):
        """Function executed when bot starts"""
        print('Logged on as', self.user)

    async def on_message(self, message):
        """What bot does when messages are sent"""
        # don't respond to ourselves
        if message.author == self.user:
            return

        if (message.content) == 'ping':
            await message.channel.send('pong')

client = MyClient(intents=intents)
intents.message_content = True # pylint: disable=assigning-non-slot
client.run(config.BOT_TOKEN)
