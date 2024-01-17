import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
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
texts = [entry["text"] for entry in training_data if entry.get("label") is not None]
labels = [entry["label"] for entry in training_data if entry.get("label") is not None]

def fetch_html_content(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5', 
    'Connection': 'keep-alive',
    }
    response = requests.get(url, headers = headers, allow_redirects=True)
    return response.text

# Function to extract text content from HTML and remove newlines
def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text_content = soup.get_text(separator=' ')
    # Replace newline characters with spaces
    text_content = text_content.replace('\n', ' ')
    return text_content

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

# Function to detect dark patterns using machine learning and MongoDB
def detect_dark_pattern_ml(html_text):
    # Extract text from HTML and remove newlines
    text_content = extract_text_from_html(html_text)
    print(f"Text Content: {text_content}")

    # Check for dark patterns based on machine learning
    text_vectorized = vectorizer.transform([text_content])
    prediction = classifier.predict(text_vectorized)
    predicted_dark_pattern = bool(prediction[0])

    if predicted_dark_pattern:
        # Find similar text in the training data
        similarities = vectorizer.transform(texts)
        similarity_scores = (text_vectorized * similarities.T).A[0]
        most_similar_index = similarity_scores.argmax()
        pattern_category = labels[most_similar_index]
        
        return True, pattern_category
    else:
        return False, None

# URL to check
url_to_check = input("Enter the link: ")
response = requests.get(url_to_check)

if response.status_code == 200:
    html_text = response.text

    # Detect dark pattern using machine learning and MongoDB
    is_dark_pattern_ml, pattern_category = detect_dark_pattern_ml(html_text)
    print(f"Dark Pattern Detected (ML): {is_dark_pattern_ml}, Pattern Category: {pattern_category}")
else:
    print(f"Failed to fetch data from URL: {url_to_check}")
