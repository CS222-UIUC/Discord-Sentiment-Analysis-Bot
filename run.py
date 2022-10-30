"""run to start bot"""

import discord_bot.bot as dbot
from discord_bot import config

dbot.bot.run(config.BOT_TOKEN)
