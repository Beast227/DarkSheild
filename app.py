from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import pygame

app = Flask(__name__)

# Initialize pygame mixer
pygame.mixer.init()

# Load the siren sound file
siren_sound = pygame.mixer.Sound("G:/DarkShield/Integraion/static/beep/beep-warning-6387.mp3")

def check_timer_issues(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        html_content = str(soup)

        if 'setInterval' in html_content:
            return True
        return False
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_timer', methods=['POST'])
def check_timer():
    try:
        url = request.form['url']
        has_timer_issues = check_timer_issues(url)

        if has_timer_issues:
            play_siren()
            return {'has_timer_issues': True, 'message': 'Warning: Potential client-side timer manipulation.'}
        return {'has_timer_issues': False, 'message': 'Timer appears to be implemented without client-side issues.'}
    except Exception as e:
        print(f"Error in check_timer endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def play_siren():
    # Play the siren sound
    siren_sound.play()

if __name__ == '__main__':
    app.run(debug=True)