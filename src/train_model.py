import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Set path to data (go up one level from /src to /data)
base_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(base_path, "data", "mbti_1.csv")

# 1. Load and prepare data
df = pd.read_csv(data_path)
X = df['posts']
y = df['type']

# 2. Balance data
min_size = df["type"].value_counts().min()

balanced_df = df.groupby("type").apply(
    lambda x: x.sample(min_size, random_state=42)
).reset_index(drop=True)

# 3. Preprocess and vectorize
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_vec = vectorizer.fit_transform(balanced_df["posts"])

# 4. Train the model
model = LogisticRegression(class_weight="balanced", max_iter=1000)
model.fit(X_vec, balanced_df["type"])

# 5. Save both model and vectorizer
joblib.dump(model, os.path.join(base_path, "src", "model.pkl"))
joblib.dump(vectorizer, os.path.join(base_path, "src", "vectorizer.pkl"))

print("✅ Training complete. Model and vectorizer saved.")
