from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

app = Flask(__name__, template_folder="web")
CORS(app, resources={r"/predict": {"origins": "http://127.0.0.1:5000"}})  # Allow cross-origin requests

# Load model and vectorizer
model = joblib.load("src/model.pkl")
vectorizer = joblib.load("src/vectorizer.pkl")

# Load test data (for accuracy display)
df = pd.read_csv("data/mbti_1.csv")
X = df["posts"]
y = df["type"]
X_vec = vectorizer.transform(X)
acc = model.score(X_vec, y)

@app.route("/")
def home():
    return render_template("index.html", accuracy=round(acc * 100, 2))  # Looks for templates/index.html

@app.route('/web/<path:filename>')
def custom_static(filename):
    return send_from_directory('web', filename)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    text = data['text']

    # Load model and vectorizer
    model = joblib.load("src/model.pkl")
    vectorizer = joblib.load("src/vectorizer.pkl")

    # Vectorize and predict
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]

    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)
