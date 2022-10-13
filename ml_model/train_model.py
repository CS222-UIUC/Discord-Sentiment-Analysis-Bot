import nltk
from nltk.tokenize import sent_tokenize, word_tokenize 
from nltk.stem import WordNetLemmatizer

def preprocess_text(input_text, stopwords):
    
    for i in range(len(stopwords)):
        stopwords[i] = stopwords[i].lower()

    preprocessed_sentences = sent_tokenize(input_text)
    preprocessed_text = []
    lemmatizer = WordNetLemmatizer()

    for sentence in preprocessed_sentences:

        tokenized_sentence = word_tokenize(sentence)

        for i in range(len(tokenized_sentence)):

            tokenized_sentence[i] = tokenized_sentence[i].lower()
        
        for i in range(len(tokenized_sentence)):

            if tokenized_sentence[i].isalpha() and tokenized_sentence[i] not in stopwords:

                tokenized_sentence[i] = lemmatizer.lemmatize(tokenized_sentence[i])
                preprocessed_text.append(tokenized_sentence[i])

    print(preprocessed_text)
    return preprocessed_text

preprocess_text("500 pennies makes $5.00 USD. $#%#$^!@#", ["The", "They", "be"])

