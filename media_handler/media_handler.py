"""Takes in unprocessed message from discord bot and processes it to work with our ML model"""
import re

def msg_to_lower(message):
    """Makes the message into all lowercase characters"""
    return message.lower()


def remove_irrelevant_chars(message):
    """Removes irrelevant characters from the message, like punctuation and other symbols"""
    return re.sub("[^a-zA-Z0-9]"," ",message)
