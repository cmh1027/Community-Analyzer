import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['pann']['host']})

def getGalleryArticleURLs(gallery_url, page=1): # 1~page까지 긁어옴
    urls = []
    for p in range(1, page+1):
        response = requests.get(gallery_url+"&page="+str(p), headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.find("ul", "list")
            for article in articles.findAll('a'):
                url = article["href"]
                urls.append("https://m.pann.nate.com" + url)
                                        
        else: 
            print(response.status_code)
            assert response.status_code != 200
    return urls

def getArticleContent(article_url):
    response = requests.get(article_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("div", "pann-title") is None: # article has been removed
        return "", ""
    else:
        return soup.find("div", "pann-title").find("h3").getText(), soup.find("div", "content").getText() # title, content