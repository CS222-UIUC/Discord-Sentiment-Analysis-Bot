import nltk
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer

def preprocess_text(input_text, stopwords):
    preprocessed_input = word_tokenize(input_text)
    for i in range(len(preprocessed_input)):
        preprocessed_input[i] = preprocessed_input[i].lower()
    for word in preprocessed_input:
        if not word.isalpha() or word in stopwords:
            preprocessed_input.remove(word)
    
    lemmatizer = WordNetLemmatizer()
    for i in range(len(preprocessed_input)):
        preprocessed_input[i] = lemmatizer.lemmatize(preprocessed_input[i])
    print(preprocessed_input)

preprocess_text("The alumni meet the criteria.", ["the"])

