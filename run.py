import discord
import config

intents = discord.Intents.default()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if (message.content) == 'ping':
            await message.channel.send('pong')

client = MyClient(intents=intents)
intents.message_content = True
client.run(config.BOT_TOKEN)
