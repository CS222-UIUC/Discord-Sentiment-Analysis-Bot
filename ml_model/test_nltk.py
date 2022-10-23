from distutils.command import clean
import nltk as nt
import pandas as pd
import numpy as np
import re
import random

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk import classify
from nltk import NaiveBayesClassifier


def read_data(filename):
    data = []
    try:
        file = open(filename,'r')
        next(file)
    except IOError:
            print("Error with file")
    else:
        for line in file:
            line = line.split(',')
            sentence = ''.join(line[-2])
            value = line[-1]
            data.append((sentence,value))
    return data

def remove_hyperlinks_and_styles(tweet):
    # removes hyperlinks with regex expressions
    new_tweet = re.sub(r'https?:\/\/.*[\r\n]*','', tweet)
    # removes hashtags
    new_tweet = re.sub(r'#','',new_tweet)
    return new_tweet

def classify_tweets(entry,category):
    value = float(entry[1].replace('\n',''))
    result = ""
    if category == '+':
        if value == 1.0:
            result = entry[0]
    elif category == '0':
        if value == 0.0:
            result = entry[0]
    elif category == '-':
        if value == -1.0:
            result = entry[0]
    return result

def tokenize_tweet(tweet):
    tweet_tokens = word_tokenize(tweet)
    return tweet_tokens

def remove_stopwords(tweet_tokens):
    unwanted = stopwords.words("english")
    unwanted.remove("not")
    unwanted.remove("we")
    clean_tweet = []
    for word in tweet_tokens:
        if (word.isalpha() and word.casefold() not in unwanted):
            clean_tweet.append(word)
    return clean_tweet

def lemmatize(clean_tweet):
    lemmatizer = WordNetLemmatizer()
    # getting lemma of each word 
    lemmatized_words = [lemmatizer.lemmatize(word,pos="v") if "ing" in word else lemmatizer.lemmatize(word)
        for word in clean_tweet]
    return lemmatized_words

def preprocess_tweet(tweet):
    tweet_clean = remove_hyperlinks_and_styles(tweet)
    tweet_tokens = tokenize_tweet(tweet_clean)
    clean_tweet = remove_stopwords(tweet_tokens)
    root_tweet = lemmatize(clean_tweet)
    return root_tweet


def get_tweets_for_model(processed_tweets):
    result = []
    for tweets in processed_tweets:
        for word_token in tweets:
            result.append({word_token : True})
    return result

def train(train,test):
    classifier = NaiveBayesClassifier.train(train)
    print(f"Classifier accuracy percent: {(classify.accuracy(classifier, test))*100}.")
    print(classifier.show_most_informative_features(10))

def main(filename):
    all_tweets = read_data(filename)
    all_pos_tweets = [classify_tweets(entry,'+') for entry in all_tweets
        if len(classify_tweets(entry,'+')) != 0]
    all_neu_tweets = [classify_tweets(entry,'0') for entry in all_tweets
        if len(classify_tweets(entry,'0')) != 0]
    all_neg_tweets = [classify_tweets(entry,'-') for entry in all_tweets
        if len(classify_tweets(entry,'-')) != 0]
    processed_pos_tweets = [preprocess_tweet(tweet) for tweet in all_pos_tweets]
    processed_neu_tweets = [preprocess_tweet(tweet) for tweet in all_neu_tweets]
    processed_neg_tweets = [preprocess_tweet(tweet) for tweet in all_neg_tweets]
    
    # Getting Data Ready for model

    pos_tweets_model = get_tweets_for_model(processed_pos_tweets)
    neu_tweets_model = get_tweets_for_model(processed_neu_tweets)
    neg_tweets_model = get_tweets_for_model(processed_neg_tweets)

    # Creating Dataset of Tuples(dict,label) and Splitting the Dataset

    pos_data = [(tweet_dict,"Positive") for tweet_dict in pos_tweets_model]
    neu_data = [(tweet_dict,"Neutral") for tweet_dict in neu_tweets_model]
    neg_data = [(tweet_dict,"Negative") for tweet_dict in neg_tweets_model]
    dataset = pos_data + neu_data + neg_data
    random.shuffle(dataset)
    train_data = dataset[:30]
    test_data = dataset[30:]
    train(train_data,test_data)

main('train_data.csv')




# def get_all_words(processed_tweets):
#     for tweet in processed_tweets:
#         for word in tweet:
#             yield word

# all_pos_words = get_all_words(processed_pos_tweets)

# freq_dist_pos = FreqDist(all_pos_words)
# print(freq_dist_pos.most_common(10))

# train_x = train_pos + train_neg
# train_y = np.append(np.ones(len(train_pos)),np.full((1,len(train_neg)),-1))

# print(f"{train_y[-1]}")

# test_x = test_pos + test_neg
# test_y = np.append(np.ones(len(test_pos)),np.full((1,len(test_neg)),-1))
