# Personality Prediction from Text (MBTI Classification)

import os
import pandas as pd
import numpy as np
import re
import string
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Dynamically find the path to the CSV
base_path = os.path.dirname(os.path.dirname(__file__))  # goes up from /src to project root
file_path = os.path.join(base_path, "data", "mbti_1.csv")

# Load the dataset
df = pd.read_csv(file_path)

print("\nData sample:")
print(df.head())

# Group by MBTI type and find the smallest group
min_size = df["type"].value_counts().min()

# Balance the dataset
balanced_df = df.groupby("type").apply(lambda x: x.sample(min_size, random_state=42)).reset_index(drop=True)

# Check class distribution
print("\nClass distribution:")
print(df['type'].value_counts())

# Optional: Limit to top 4 types for simplicity
top_types = df['type'].value_counts().nlargest(4).index
df = df[df['type'].isin(top_types)]

# Preprocessing text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+', '', text)  # remove links
    text = re.sub(r'[^a-z\s]', '', text)      # remove punctuation and numbers
    text = re.sub(r'\s+', ' ', text)          # remove extra spaces
    return text.strip()

df['clean_posts'] = df['posts'].apply(clean_text)

# Split data
X = df['clean_posts']
y = df['type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=3000)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Prediction
y_pred = model.predict(X_test_tfidf)

# Evaluation
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Confusion Matrix
plt.figure(figsize=(8,6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', xticklabels=top_types, yticklabels=top_types)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("MBTI Personality Type Prediction")
plt.tight_layout()
plt.show()
