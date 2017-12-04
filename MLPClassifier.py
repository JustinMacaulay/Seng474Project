import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MaxAbsScaler
from sklearn.metrics import classification_report, confusion_matrix

train = pd.read_csv("Tweets/tweet4-even-train.csv", engine="python", encoding="utf-8")
test = pd.read_csv("Tweets/tweet4-even-test.csv", engine="python", encoding="utf-8")

vectorizer = CountVectorizer(
    input='content',
    stop_words='english',
    max_df=1.0,
    min_df=1,
    binary=False
)

vectorizer.fit(pd.concat([train.text, test.text]).values)

X_train = vectorizer.transform(train.text.values)
y_train = train.id.values

X_test = vectorizer.transform(test.text.values)
y_test = test.id.values

test.id.unique()

mlp = MLPClassifier(
    max_iter=100,
    hidden_layer_sizes=(500, 200, 30, len(test.id.unique()))
)

mlp.fit(X_train, y_train)

predictions = mlp.predict(X_test)

print("Train set size: {}\nTest set size: {}".format(X_train.shape, X_test.shape))

print(confusion_matrix(y_test, predictions))

print(classification_report(y_test, predictions))
