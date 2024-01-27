import requests
from bs4 import BeautifulSoup

ids = {"dealBadgeSupportingText"}
classes = {"_2JC05C", "sc-dkrFOg kAJwOV"}

def scraping_text(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for id in ids : 
            element = soup.find(id=id)
            if element:
                    text_inside = element.get_text(strip=True)
                    
                    if text_inside:
                        return text_inside
        else : 
             for c in classes:
                  element = soup.find(class_ = c)

                  if element:
                    text_inside = element.get_text(strip=True)
                
                    if text_inside:
                        return text_inside
    return None
#timer functions
def check_timer_issues(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        html_content = str(soup)

        if 'setInterval' in html_content:
            return True
        return False
    else:
        return False