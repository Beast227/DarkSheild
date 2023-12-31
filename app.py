import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

nltk.download('punkt')
nltk.download('stopwords')

with open("dark_patterns.json", "r") as json_file:
    dark_patterns_data = json.load(json_file)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.dark_patterns_db
collection = db.dark_patterns

# Load existing data for training
training_data = list(collection.find({}))

# Tokenization and feature extraction
texts = [entry["text"] for entry in training_data]

# Check if 'dark_pattern_detected' key is present in entries
labels = [entry.get("dark_pattern_detected", None) for entry in training_data]

# Remove entries where 'dark_pattern_detected' is None
filtered_data = [(text, label) for text, label in zip(texts, labels) if label is not None]
texts, labels = zip(*filtered_data)

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

# Train a simple classifier (Naive Bayes in this example)
classifier = MultinomialNB()
classifier.fit(X, labels)

def detect_dark_pattern_ml(text):
    # Use the trained model to predict dark pattern
    text_vectorized = vectorizer.transform([text])
    prediction = classifier.predict(text_vectorized)
    return bool(prediction[0])

def detect_false_urgency(element_data):
    # Check if the conditions for false urgency are met
    timer_condition = element_data.get("timer", {}).get("remainingSeconds", 0) == 0
    text_condition = "Limited-time offer! Act now!" in element_data.get("text", "").lower()

    return timer_condition and text_condition

def apply_dark_pattern_detection(json_data, html_template):
    for pattern in json_data.get("darkPatterns", []):
        if pattern["logic"]["trigger"] == "falseUrgency":
            if detect_false_urgency(html_template):
                print(f"Dark pattern detected: {pattern['name']}")
                # Here you could take action, log, or modify the HTML accordingly
                # For this example, let's print a warning message
    
    # In a real-world scenario, you might want to return or modify the HTML accordingly

def analyze_and_update_dark_patterns_advanced(data):
    for entry in data:
        website = entry["name"]
        text = entry["text"]
        html_code = entry.get("html_code", "")  # Assume "html_code" field in documents

        # Extract text content from HTML code using BeautifulSoup
        soup = BeautifulSoup(html_code, 'html.parser')
        html_text = soup.get_text()

        # Combine text and HTML content for analysis
        combined_text = f"{text} {html_text}"

        # Detect dark pattern using machine learning
        is_dark_pattern_ml = detect_dark_pattern_ml(combined_text)

        # Save the analysis result back to the database
        collection.update_one({"name": website}, {"$set": {"dark_pattern_detected_ml": is_dark_pattern_ml}})

        print(f"Website: {website}\nText: {text}\nHTML Code: {html_code}\nDark Pattern Detected (ML): {is_dark_pattern_ml}\n")

def check_dark_pattern_for_url(url):
    # Make a request to the given URL
    response = requests.get(url)
    if response.status_code == 200:
        # Extract text content from the HTML response
        html_code = response.text
        soup = BeautifulSoup(html_code, 'html.parser')
        text = soup.get_text()

        # Detect dark pattern using machine learning
        is_dark_pattern_ml = detect_dark_pattern_ml(text)

        print(f"URL: {url}\nText: {text}\nDark Pattern Detected (ML): {is_dark_pattern_ml}\n")

        # Check for dark patterns based on predefined rules
        html_template = {"timer": {"remainingSeconds": 0}, "text": text}
        apply_dark_pattern_detection(dark_patterns_data, html_template)

        # Save the analysis result to the database
        collection.insert_one({"name": url, "text": text, "dark_pattern_detected_ml": is_dark_pattern_ml})
    else:
        print(f"Failed to fetch data from URL: {url}")

# Example usage:
url_to_check = input("Enter the link: ")
check_dark_pattern_for_url(url_to_check)