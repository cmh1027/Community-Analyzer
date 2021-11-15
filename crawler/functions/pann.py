import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from functions.crawler_decorator import url_crawler, article_crawler
import utility.constant as constant

@url_crawler
def getGalleryArticleURLs(gallery_url, page, headers): # article_max 개의 게시글을 긁어옴
    urls = []
    response = requests.get(gallery_url+"&page="+str(page), headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find("ul", "list")
        urls = []
        for article in articles.findAll('a'):
            urls.append("https://m.pann.nate.com" + article["href"])
    return (response.status_code, urls)

@article_crawler
def getArticleContent(soup):
    title = soup.find("div", "pann-title")
    if title is None: # article has been removed
        return "", ""
    else:
        return title.find("h3").getText(), soup.find("div", "content").getText() # title, content