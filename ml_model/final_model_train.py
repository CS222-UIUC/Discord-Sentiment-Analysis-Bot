"""
    Training Sentiment Analysis Model using TFIDF Vectorizer and
    different classifiers (SVM, Logisitic Regression, Random Forest)
    to obtain the highest accuracy

"""
import re
import warnings
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer as tfidf
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
# from sklearn.metrics import log_loss
from sklearn import metrics
warnings.simplefilter(action='ignore', category=FutureWarning)

# For AZURE SERVERS
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


def read_data(filename):
    """
        Reads data from csv file.

        This function reads the data into a pandas dataframe
        making the first line the headers and removes any empty rows
        Resets indices and turns polarity score into int
        Creates a random sample of 90k tweets (30k pos 30k neu 30k neg)

        Parameters
        ----------
        filename : string
            filename of dataset
        Returns
        -------
        dataframe {Tweet : Polarity}
            The raw tweet and it's polarity
    """
    data = pd.read_csv(filename, header=0, dtype=str)
    data = data.dropna()
    data = data.reset_index(drop=True)
    data = data.rename(columns={"comment" : "Tweet", "category" : "Polarity"})
    data['Polarity'] = data['Polarity'].astype(float)
    # 1.0 - 109011 entries
    # 0.0 99693 entries
    # -1.0 66410 entries
    # Shuffles and gets a 45k of each
    data = data.sample(frac=1, random_state=1).reset_index(drop=True) # shuffles all tweets
    sample = data[data['Polarity'] == 1.0][:60000]
    sample = sample.append(data[data['Polarity'] == 0.0][:60000])
    sample = sample.append(data[data['Polarity'] == -1.0][:60000])
    sample = sample.reset_index(drop=True)
    return sample

def remove_hyperlinks_and_styles(tweet):
    """
        Removes hyperlinks and other styles from tweet

        Parameters
        ----------
        tweet : string
            tweet from dataframe
        Returns
        -------
        tweet : string
            The cleaned tweet
    """
    # removes hyperlinks with regex expressions
    new_tweet = re.sub(r'https?:\/\/.*[\r\n]*','', tweet)
    # removes hashtags
    new_tweet = re.sub(r'#','',new_tweet)
    return new_tweet

def remove_stopwords(tweet_tokens):
    """
        Removes unnecessary words or any non-alpha characters

        Parameters
        ----------
        clean_tweet : string
        Returns
        -------
        lemmatized_tweet : string
            The lemmatized tweet with each word in its root form
    """
    unwanted = stopwords.words("english")
    unwanted.remove("not")
    unwanted.remove("we")
    clean_tweet = []
    for word in tweet_tokens:
        if (word.isalpha() and word.casefold() not in unwanted):
            clean_tweet.append(word)
    return clean_tweet

def lemmatize(clean_tweet):
    """
        Lemmatizes each word in tweet transforming them
        into their root form

        Parameters
        ----------
        clean_tweet : string
        Returns
        -------
        lemmatized_tweet : string
            The lemmatized tweet with each word in its root form
    """
    lemmatizer = WordNetLemmatizer()
    # getting lemma of each word
    lemmatized_words = [lemmatizer.lemmatize(word,pos="v")
        if "ing" in word else lemmatizer.lemmatize(word)
            for word in clean_tweet]
    result = ' '.join(lemmatized_words)
    return result

def preprocess_tweet(tweet):
    """
        Preprocesses tweet by removing hyperlinks, stopwords, and
        transforming tweet into root form

        Parameters
        ----------
        tweet : string
        Returns
        -------
        root_tweet : string
            The cleaned and root form of the tweet
    """
    tweet_clean = remove_hyperlinks_and_styles(tweet)
    tweet_tokens = word_tokenize(tweet_clean) # list of every word in tweet
    clean_tweet = remove_stopwords(tweet_tokens) # removes stopwords
    root_tweet = lemmatize(clean_tweet) # sentence with root lemma words
    return root_tweet

def preprocessing(sample_data):
    """
        Adds preprocessed tweets into a new Preprocessed column in dataframe

        Parameters
        ----------
        dataframe : {Tweet : Polarity}
        Returns
        -------
        dataframe : {Tweet : Polarity : Preprocessed}
            The cleaned root form of the tweet
    """
    sample_data["Preprocessed"] = [preprocess_tweet(str(x)) for x in sample_data["Tweet"]]
    return sample_data

def train_model(clean_tweets_data, classifiers_list):
    """
        Generates model based on the requested classifier with a TFIFD Vectorizer
        Reports accuracy scores for each polarity and the final accuracy

        Parameters
        ----------
        dataframe : {Tweet : Polarity : Preprocessed}
        classifiers : array of strings that say which classifiers used
        Void Return

        Prints
        --------
            All Classifier Reports
            Final Accuracy of Model
    """
    # Splitting cleaned tweets into train and test data
    x_train, x_test, y_train, y_test = train_test_split(clean_tweets_data['Preprocessed'],
        clean_tweets_data['Polarity'], test_size=0.25, random_state=30)
    # print(f"Train: {x_train.shape,y_train.shape} Test: {x_test.shape,y_test.shape}")

    # TFIDF Vectorizer
    vectorizer = tfidf()
    tf_x_train = vectorizer.fit_transform(x_train)
    tf_x_test = vectorizer.transform(x_test)
    for classifier in classifiers_list:
        if classifier == "svm":
            clf = LinearSVC(random_state=0)
            clf.fit(tf_x_train, y_train)
            y_test_pred = clf.predict(tf_x_test)
            report = classification_report(y_test, y_test_pred,output_dict=True)
            print("SVM Accuracy Report")
            print(report)
            print("\nAccuracy for SVM :",metrics.accuracy_score(y_test, y_test_pred))
        elif classifier == "log":
            clf = LogisticRegression(max_iter=1000,solver="saga")
            clf.fit(tf_x_train, y_train)
            y_test_pred = clf.predict(tf_x_test)
            report = classification_report(y_test, y_test_pred,output_dict=True)
            print("Logisitic Regression Report")
            print(report)
            print("\nAccuracy for Log :",metrics.accuracy_score(y_test, y_test_pred))
        elif classifier == "rfc":
            # From AZURE (17 min 31s):
            clf = RandomForestClassifier(n_estimators=150)
            clf.fit(tf_x_train, y_train)
            y_test_pred = clf.predict(tf_x_test)
            report = classification_report(y_test, y_test_pred,output_dict=True)
            print("Random Forest Classifier Report")
            print(report)
            print("\nAccuracy for RFC :",metrics.accuracy_score(y_test, y_test_pred))
            # Accuracy: 0.8053925925925925
            # depths = [tree.tree_.max_depth for tree in clf.estimators_]
            # import numpy as np
            # print(f"Mean tree depth in the Random Forest: {np.round(np.mean(depths))}")
            # Mean tree depth in the Random Forest: 2587.0
            clf_cap = RandomForestClassifier(n_estimators=150, max_depth=2500)
            clf_cap.fit(tf_x_train, y_train)
            y_test_pred_cap = clf_cap.predict(tf_x_test)
            print("\nAccuracy for RFC(max_d=2500):",metrics.accuracy_score(y_test, y_test_pred_cap))
    # clf_loss = log_loss(y_test, y_test_pred)
    # print(clf_loss)

def predict_tweet(tweet, clean_data, classifer):
    
    # Creating a SVM Model (In our case this model would have been already created)
     x_train, x_test, y_train, y_test = train_test_split(clean_data['Preprocessed'],
        clean_data['Polarity'], test_size=0.25, random_state=30)
    
    # TFIDF Vectorizer
    vectorizer = tfidf()
    tf_x_train = vectorizer.fit_transform(x_train)
    tf_x_test = vectorizer.transform(x_test)
    # For our single tweet (create vectorizer and transform)
    tf_tweet_test = vectorizer.transform(tweet)
    
    clf = LinearSVC(random_state=0)
    clf.fit(tf_x_train, y_train)
    y_test_pred = clf.predict(tf_x_test)
    # single tweet prediction
    tweet_predict = clf.predict(tf_tweet_test)
    report = classification_report(y_test, y_test_pred,output_dict=True)
    print("SVM Accuracy Report")
    print(report)
    print("\nAccuracy for SVM :",metrics.accuracy_score(y_test, y_test_pred))
    # What Model Predicted Polarity of Tweet to be (An array)
    print("\nPolarity of Single tweet:",tweet_predict)
    

frac = read_data("fixed_final_dataset.csv")
clean_tweets = preprocessing(frac)
# print(frac['Polarity'].value_counts())

classifiers = ["svm", "log", "rfc"]
train_model(clean_tweets,classifiers)
text =  "I love animals so much!"
predict_classifiers = ["svm"]
cleaned_tweet = preprocess_tweet(text, clean_tweets, predict_classifiers)
