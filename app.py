from flask import Flask, render_template, request, jsonify
from ml_model.scraper import check_timer_issues, find_text_by_ids
from ml_model.predict import predict_pattern_category
from bs4 import BeautifulSoup
import requests
import pygame

app = Flask(__name__)

# Initialize pygame mixer
pygame.mixer.init()

# Load the siren sound file
true_sound = pygame.mixer.Sound("G:/DarkShield/Integraion/static/audio/detected.mp3")
false_sound = pygame.mixer.Sound("G:/DarkShield/Integraion/static/audio/notdetected.mp3")

@app.route('/')
def log():
    return render_template('log.html')

@app.route('/index_html', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/check_timer', methods=['POST'])
@app.route('/check_timer', methods=['POST'])
def check_timer():
    try:
        url = request.form['url']
        has_timer_issues = check_timer_issues(url)

        if has_timer_issues:
            # Extract the text from the URL
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            html_content = str(soup)
            text = find_text_by_ids(html_content)

            # Predict the pattern category of the text
            pattern_category = predict_pattern_category(text)

            # Play the sound based on the pattern category
            if pattern_category == 'False Urgency':
                false_sound.play()
            else:
                true_sound.play()

            print(pattern_category)
            return jsonify({'success': True, 'pattern_category': pattern_category})
        else:
            false_sound.play()
            return jsonify({'success': True})
    except Exception as e:
        print(f"Error in check_timer endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
