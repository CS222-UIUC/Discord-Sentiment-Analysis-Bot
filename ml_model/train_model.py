import nltk
from nltk.tokenize import sent_tokenize, word_tokenize 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
stopword_list = stopwords.words('english')

def preprocess_text(input_text):
    global stopword_list
    for i in range(len(stopword_list)):
        stopword_list[i] = stopword_list[i].lower()

    preprocessed_sentences = sent_tokenize(input_text)
    preprocessed_text = []
    lemmatizer = WordNetLemmatizer()

    for sentence in preprocessed_sentences:

        tokenized_sentence = word_tokenize(sentence)
        
        for i in range(len(tokenized_sentence)):
            
            tokenized_sentence[i] = tokenized_sentence[i].lower()


            if tokenized_sentence[i].isalpha() and tokenized_sentence[i] not in stopword_list:

                tokenized_sentence[i] = lemmatizer.lemmatize(tokenized_sentence[i])
                preprocessed_text.append(tokenized_sentence[i])

    print(preprocessed_text)
    #print(stopword_list)
    return preprocessed_text

preprocess_text("You'll always be able to do it.")

