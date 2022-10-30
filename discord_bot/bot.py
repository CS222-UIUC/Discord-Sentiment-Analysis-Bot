"""Bot"""
import random
import config
import discord

bot = discord.Client()

#################################
# remove after model is complete
def determine_sentiment(message):
    """
    Arguments:
        message: message content from discord message
    Returns:
        sentiment -1, 0, 1
    """
    print(message)
    return random.randint(-1,1)
################################

@bot.event
async def on_ready():
    """
    Arguments:
        message: runs on ready
    Returns:
        Nothing
    """
    # start up model
    input_activity = discord.Activity(type=discord.ActivityType.watching, name='your comments 👀')
    await bot.change_presence(activity=input_activity)
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    """
    brains of the discord bot
    Arguments:
        message: message from discord picked up by API
    Returns:
        will react according to messages sent by user. defined below
    """
    # 10% chance to change bot status for each message
    change_selection = random.randint(0,9)
    if not change_selection:
        selection = random.randint(0,2)
        new_status = config.STATUS_CHANGE[selection]

        print("status changed to: ", new_status)
        await bot.change_presence(activity=discord.Activity(type=new_status[0], name=new_status[1]))
    if message.author == bot.user:
        return

    if message.content == "-help":
        await message.channel.send(embed = config.HELP_EMBED)
    else:
        sentiment = determine_sentiment(message.content)
        print(sentiment) # for debugging purposes
        if sentiment == 1:
            await message.add_reaction('👍')
        elif sentiment == 0:
            await message.add_reaction('👊')
        else: # sentiment == -1
            await message.add_reaction('👎')


bot.run(config.BOT_TOKEN)
