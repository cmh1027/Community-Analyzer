import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['pann']['host']})

def getGalleryArticleURLs(gallery_url, article_max=1): # article_max 개의 게시글을 긁어옴
    urls = []
    page = 1
    article_num = 0
    while True:
        response = requests.get(gallery_url+"&page="+str(page), headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.find("ul", "list")
            if len(articles) == 0:
                return urls
            for article in articles.findAll('a'):
                url = article["href"]
                urls.append("https://m.pann.nate.com" + url)
                article_num += 1
                if article_num >= article_max:
                    return urls
        else: 
            print(response.status_code)
            assert response.status_code != 200
        page += 1

def getArticleContent(article_url):
    response = requests.get(article_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("div", "pann-title") is None: # article has been removed
        return "", ""
    else:
        return soup.find("div", "pann-title").find("h3").getText(), soup.find("div", "content").getText() # title, content