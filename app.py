from flask import Flask, render_template, request, jsonify
from ml_model.scraper import check_timer_issues, scraping_text
from ml_model.predict import predict_pattern_category
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

@app.route('/check_pattern', methods=['POST','GET'])
def check_timer():
    try:
        url = request.form['url']
        has_timer_issues = check_timer_issues(url)

        text = scraping_text(url)
        if text : 
            pattern_category = predict_pattern_category(text)
        else : 
            pattern_category = "No Dark Pattern found"

        if has_timer_issues:
            false_sound.play()
        else:
            true_sound.play()

        return render_template('index.html',message = pattern_category)
    
    except Exception as e:
        print(f"Error in check_pattern endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
