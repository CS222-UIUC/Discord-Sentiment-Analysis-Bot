"""Takes in unprocessed message from discord bot, processes it to work with ML model,
passes it to ML & returns the sentiment of the message"""

def remove_irrelevant(message):
    """Removes irrelevant characters from the message such at @ & punctuation"""
    return message
