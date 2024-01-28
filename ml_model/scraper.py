import requests
from bs4 import BeautifulSoup

ids = {"dealBadgeSupportingText"}
classes = {"_2JC05C", "sc-dkrFOg kAJwOV","css-1d0jf8e","css-1kzcg63","custom-tag"," css-1bse542","css-wkluxr","css-cjd9an","css-dsmh93","css-4ifat7", "css-1antjnx","css-1oh7ecm","css-nbi20s","css-za4feu",
"of-lable fanB"," ng-star-inserted","css-fcdoej","css-1sgl9hr","css-901oao r-1awozwy r-jwli3a r-1vgyyaa r-1gkfh8e r-q4m81j","css-901oao r-1vgyyaa r-10x49cs r-1rsjblm r-l4nmg1 r-m2pi6t r-1hvjb8t r-vmopo1","css-901oao"," r-1kihuf0"," r-1w427b9"," r-1vgyyaa"," r-1b43r93"," r-1rsjblm"," r-11wrixw"," r-q4m81j"," r-1vzi8xi","promo-desc",
"dIb vM cdL m04 fs12","pdpDiscount ","product-discount","wt-mb-xs-1", "wt-mt-xs-1","ShippingInfo__StyledDealsTimer-sc-frp12n-10"," lklfEE","css-901oao"," r-op4f77"," r-1vgyyaa"," r-10x49cs"," r-1cwl3u0","d-quantity__availability",
"vim d-sme-atf","vi-notify-new-bg-dBtm"
}

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