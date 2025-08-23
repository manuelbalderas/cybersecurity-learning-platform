import pandas as pd
from sklearn.model_selection import train_test_split

import joblib

df = pd.read_csv('data/ml_messages.csv')

X = df['Message']
y = df['Classification']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
spanish_stopwords = stopwords.words('spanish')

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words=spanish_stopwords)  # Use Spanish stop words
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# BAYES - 0.85665
# from sklearn.naive_bayes import MultinomialNB
# model = MultinomialNB()
# model.fit(X_train_tfidf, y_train)

# SVM LINEAR - 0.86689
# from sklearn.svm import SVC
# model = SVC(kernel='linear')
# model.fit(X_train_tfidf, y_train)

# LINEAL - 0.84122
# from sklearn.linear_model import LogisticRegression
# model = LogisticRegression(max_iter=1000)
# model.fit(X_train_tfidf, y_train)

# KNN - 0.8276
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

from sklearn.metrics import accuracy_score, classification_report
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))

my_string = "¿Qué es una vulnerabilidad, como un zapato?" 
my_string_tfidf = vectorizer.transform([my_string])
my_pred = model.predict(my_string_tfidf)
print(f"Prediccion: {my_pred[0]}")

# joblib.dump(model, 'models/knn_model.joblib')
# joblib.dump(vectorizer, 'models/tfidf_vectorizer.joblib')