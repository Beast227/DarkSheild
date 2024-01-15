from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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
    url = request.form['url']
    has_timer_issues = check_timer_issues(url)
    return jsonify({'has_timer_issues': has_timer_issues})

if __name__ == '__main__':
    app.run(debug=True)