from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import pygame

app = Flask(__name__)

# Initialize pygame mixer
pygame.mixer.init()

# Load the siren sound file
true_sound = pygame.mixer.Sound("C:\\Users\\ABHEESHTA\\Desktop\\DarkSheild\\static\\audio\\detected.mp3")
false_sound = pygame.mixer.Sound("C:\\Users\\ABHEESHTA\\Desktop\\DarkSheild\\static\\audio\\notdetected.mp3")

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
def log():
    return render_template('log.html')

@app.route('/index_html', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/check_timer', methods=['POST'])
def check_timer():
    try:
        url = request.form['url']
        has_timer_issues = check_timer_issues(url)

        if has_timer_issues:
            true_sound.play()
        else:
            false_sound.play()

        # Add a return statement here to return a response
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error in check_timer endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
