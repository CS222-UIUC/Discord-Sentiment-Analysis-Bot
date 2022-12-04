"""bot.py"""
# import pytest
# import discord.ext.test as dpytest
import random
from discord.ext import commands
from discord import Intents
import config
import discord
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer

import nltk
nltk.download('punkt')

bot = commands.Bot("-", intents=Intents().all())

model, bag_of_words = None, None

@bot.command()
async def ping(ctx):
    """
    generic test function
    """
    await ctx.send("pong")

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    bag_of_words = pickle.load(f)

def determine_sentiment(message):
    """
    Arguments:
        test: message content from discord message
    Returns:
        sentiment -1, 0, 1
    """
    global bag_of_words
    global model

    test = [message]
    # test = ["I hate this stupid movie."]
    test_text = bag_of_words.transform(test)
    predictions = model.predict(test_text)
    
    return int(float(predictions[0]))

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
