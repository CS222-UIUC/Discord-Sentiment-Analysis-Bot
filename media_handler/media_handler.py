"""Takes in unprocessed message from discord bot and processes it to work with our ML model, use """
import re
import nltk #pylint: disable=W
import sklearn #pylint: disable=W E
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer #pylint: disable=E
from nltk.stem import WordNetLemmatizer #pylint: disable=C
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords_list = stopwords.words('english')

#Function to use
def process_message(message):
    """The main function to call and process a message"""
    message = msg_to_lower(message)
    message = remove_irrelevant_chars(message)
    message = process_using_nltk(message)
    bow = CountVectorizer(tokenizer=word_tokenize,stop_words=stopwords_list)
    vector = bow.fit_transform(message)
    return vector

#Helpers
def msg_to_lower(message):
    """Makes the message into all lowercase characters"""
    return message.lower()


def remove_irrelevant_chars(message):
    """Removes irrelevant characters from the message, like punctuation and other symbols"""
    message = re.sub("[^a-zA-Z0-9]"," ",message)
    message = re.sub("\n", " ", message)
    return message

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
            if word not in stopwords_list:
                tokenized_processed_message.append(lemmatizer.lemmatize(word))

    return tokenized_processed_message
