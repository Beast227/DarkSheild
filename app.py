import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

nltk.download('punkt')
nltk.download('stopwords')

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.dark_patterns_db
collection = db.dark_patterns

# Load existing data for training
training_data = list(collection.find({}))

# Tokenization and feature extraction
texts = [entry["text"] for entry in training_data if entry.get("dark_pattern_detected", None) is not None]
labels = [entry["dark_pattern_detected"] for entry in training_data if entry.get("dark_pattern_detected", None) is not None]

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

# Train a simple classifier (Naive Bayes in this example)
classifier = MultinomialNB()
classifier.fit(X, labels)

def detect_dark_pattern_ml(html_text, pattern_data):
    # Check for dark patterns based on machine learning
    text_vectorized = vectorizer.transform([html_text])
    prediction = classifier.predict(text_vectorized)
    is_dark_pattern_ml = bool(prediction[0])

    for dark_patterns in pattern_data : 
        if dark_patterns.get("dark_pattern_detected", False):
            print(f"Dark pattern detected: {dark_patterns['text']}")

    return is_dark_pattern_ml

# Example usage:
url_to_check = input("Enter the link: ")
response = requests.get(url_to_check)

if response.status_code == 200:
    html_text = BeautifulSoup(response.text, 'html.parser').get_text()

    # Retrieve the specific dark pattern data for the provided URL
    pattern_data = collection.find()

    if pattern_data:
        # Detect dark pattern using machine learning and predefined rules for the current pattern
        is_dark_pattern_ml = detect_dark_pattern_ml(html_text, pattern_data)
        print(f"Dark Pattern Detected (ML): {is_dark_pattern_ml}")

        # Save the analysis result to the database
        collection.insert_one({
            "name": url_to_check,
            "text": html_text,
            "dark_pattern_detected_ml": is_dark_pattern_ml
        })
    else:
        print(f"No dark patterns data found for the provided URL. Exiting.")
else:
    print(f"Failed to fetch data from URL: {url_to_check}")
