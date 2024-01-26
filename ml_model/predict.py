import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Define the preprocess_text function
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(text.lower())
    filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(filtered_tokens)


def predict_pattern_category(text) : 
    # Load the trained model and vectorizer from the pickle file
    with open('ml_model/model.pkl', 'rb') as f:
        model = pickle.load(f)
        vectorizer = pickle.load(f)

    # Preprocess the new text
    preprocessed_text = preprocess_text(text)

    # Vectorize the preprocessed text using the same TF-IDF vectorizer
    new_text_tfidf = vectorizer.transform([preprocessed_text]).toarray()

    # Use the trained model to predict the category
    predicted_category = model.predict(new_text_tfidf)[0]

    return predicted_category