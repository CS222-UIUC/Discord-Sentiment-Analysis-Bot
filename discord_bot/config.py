"""Standard config file for discord bot"""
import discord

BOT_TOKEN: str = "MTAxNjUyMDE5MDIzOTk4MTcxOA.G3nJMb.34AiYyYpXCs_bD64OG2ZZ7vUxjIHQRtmmv5vcY"
BOT_PREFIX = "-"

STARTUP_MESSAGE = "Starting Bot..."
STARTUP_COMPLETE_MESSAGE = "Startup Complete"

HELP_PING_SHORT = "Pong"
HELP_PING_LONG = "Test bot response status"

HELP_EMBED = discord.Embed()
HELP_EMBED.add_field(name="ML BOT 38", value=
"""Hello!

I am ML Bot 38! I was developed by CS222 group 38!
I use machine learning to determine what kind of message you send.

So far, I will react with the following responses:
        👍 : positive comment
        👊 : neutral comment
        👎 : negative comment

Keep commenting to see what I think of your message!""")

STATUS_CHANGE = [(discord.ActivityType.watching, "your comments 👀"),
                 (discord.ActivityType.listening, "the server"),
                 (discord.ActivityType.listening, "your every move")
]
