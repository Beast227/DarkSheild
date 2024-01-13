import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import re

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

def extract_timer_text(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    # Specify the regular expression to find tags with relevant attributes
    timer_tags = soup.find_all(re.compile(r'timer|time|span|div|p', re.I), class_='timer-class')

    timer_text_list = []
    for tag in timer_tags:
        # Extract the text content and append to the list
        timer_text_list.append(tag.get_text())

    return ' '.join(timer_text_list)  # Join the list into a single string


# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
X_train_vectorized = vectorizer.fit_transform(X_train)
X_valid_vectorized = vectorizer.transform(X_valid)

# Check if there is any non-empty document after vectorization
if X_train_vectorized.shape[0] == 0:
    raise ValueError("No non-empty documents after vectorization. Check your data preprocessing.")

# Train a classifier (Naive Bayes in this example)
classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)

# Evaluate the model on the validation set
y_valid_pred = classifier.predict(X_valid_vectorized)
accuracy = accuracy_score(y_valid, y_valid_pred)
print(f"Validation Accuracy: {accuracy * 100:.2f}%")

def detect_dark_pattern_ml(html_text, pattern_data):
    # Extract timer text
    timer_text = extract_timer_text(html_text)
    print(f"Timer Text: {timer_text}")

    # Check for dark patterns based on machine learning
    text_vectorized = vectorizer.transform([timer_text])
    prediction = classifier.predict(text_vectorized)
    predicted_dark_pattern = bool(prediction[0])

    for dark_patterns in pattern_data:
        if dark_patterns.get("dark_pattern_detected", False):
            print(f"Dark pattern detected: {dark_patterns['text']}")
            if dark_patterns['text'].lower() in timer_text.lower():
                print("Match found with timer text!")
                return True

    return predicted_dark_pattern

url_to_check = input("Enter the link: ")
response = requests.get(url_to_check)

if response.status_code == 200:
    html_text = response.text

    # Retrieve the specific dark pattern data for the provided URL
    pattern_data = list(collection.find())

    if pattern_data:
        # Extract timer text and detect dark pattern using machine learning
        timer_text = extract_timer_text(html_text)
        print(f"Timer Text: {timer_text}")
        
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