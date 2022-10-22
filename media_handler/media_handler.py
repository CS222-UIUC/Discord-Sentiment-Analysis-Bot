"""Takes in unprocessed message from discord bot and processes it to work with our ML model"""
import re
import nltk #pylint: disable=W
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

def msg_to_lower(message):
    """Makes the message into all lowercase characters"""
    return message.lower()


def remove_irrelevant_chars(message):
    """Removes irrelevant characters from the message, like punctuation and other symbols"""
    return re.sub("[^a-zA-Z0-9]"," ",message)

def process_using_nltk(message):
    """Tokenizes & processes a message using nltk,
    removes stop words & lemmatizes each word in message"""
    #Tokenize by sentences in case message is more than one sentence
    sentences = sent_tokenize(message)
    #Initialize empty list that will contain our final processed message
    tokenized_processed_message = []
    #Set lemmatizer
    lemmatizer = WordNetLemmatizer()
    #Loop to process each sentence & append it to list with processed message
    for sen in sentences:
        #toeknize sentence by words
        words = word_tokenize(sen)
        #Add lematized words to tokenized message & remove stopwords
        for word in words:
            if word not in stopwords:
                tokenized_processed_message.append(lemmatizer.lemmatize(word))

    print(tokenized_processed_message)
    return tokenized_processed_message
