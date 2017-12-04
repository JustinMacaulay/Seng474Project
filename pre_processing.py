import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MaxAbsScaler
from sklearn.metrics import classification_report, confusion_matrix
from flask import jsonify

class pre_processing():
    classifier = None
    vectorizer = CountVectorizer(
        input='content',
        stop_words='english',
        max_df=1.0,
        min_df=1,
        binary=False
    )
    def __init__(self):
        train = pd.read_csv("Tweets/tweet4-even-train.csv", engine="python", encoding="utf-8")

        print("preparing training...\n")
        self.vectorizer.fit(pd.concat([train.text]).values)
        print("vectorizing complete")
        X_train = self.vectorizer.transform(train.text.values)
        y_train = train.id.values

        self.classifier = MLPClassifier(
            max_iter=100,
            hidden_layer_sizes=(500, 200, 30, len(train.id.unique()))
        )
        print("training complete")
        self.classifier.fit(X_train, y_train)
        print("classification completed")

    def test(self, tweet_text):
        n = self.vectorizer.transform([tweet_text])
        probabilities = self.classifier.predict_proba(n)
        prediction = self.classifier.predict(n)
        response = {
            "tweet": tweet_text,
            "prediction_ellen": probabilities[0][0],
            "prediction_elon": probabilities[0][1],
            "prediction_obama": probabilities[0][2],
            "prediction_trump": probabilities[0][3],
            "prediction": prediction[0]
        }
        return jsonify(response)
