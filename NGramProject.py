import numpy as np
import pandas as pd
import nltk
from sklearn.feature_extraction.text import CountVectorizer

def stemAndRemovePuncAndStopWords(data):

    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    sno = nltk.stem.SnowballStemmer('english')

    for tweet in data:
        for word in tokenizer.tokenize(tweet):
            sno.stem(word)


    return [" ".join([sno.stem(word) for word in tokenizer.tokenize(tweet)]for tweet in data)]

#if word not in nltk.corpus.stopwords.words('english')

#Read in the data to a pandas DataFrame
train = pd.read_csv("Tweets/tweet4-even-train.csv", encoding="utf-8")
test = pd.read_csv("Tweets/tweet4-even-test.csv", encoding="utf-8")

def buildFeatureSet(data):
    vectorizer = CountVectorizer(
        lowercase=True,
        stop_words=None,
        max_df=25,
        min_df=1,
        max_features=None,
        binary=True,
        ngram_range=(2,2)
    )

    features = vectorizer.fit_transform(data['text'].values.astype('U')).toarray()
    feature_names = vectorizer.get_feature_names()
    print("Vocab size: {}".format(len(feature_names)))

    return list(zip(
        [  # zip a list of vocab dicts with their genre
            {
                word: bool(features[row][idx])  # A word and its presence in this song
                for idx, word in enumerate(feature_names)  # Go through all the words in the vocab
            } for row in range(len(features))  # Each dict has |vocab| entries: true or false if the song has that word
        ],data['id']
    ))

train = buildFeatureSet(train)
test = buildFeatureSet(test)

classifier = nltk.NaiveBayesClassifier.train(train)

classifier.show_most_informative_features()
nltk.classify.accuracy(classifier, test)
