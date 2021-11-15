import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from functions.crawler_decorator import url_crawler, article_crawler
import utility.constant as constant

@url_crawler
def getGalleryArticleURLs(gallery_url, page, headers): # article_max 개의 게시글을 긁어옴
    response = requests.get(gallery_url+"?od=T31&category=0&po="+str(page), headers=headers)
    urls = []
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.findAll("a", "list_subject")
        if len(articles) >= 1:
            articles = articles[1:]
        for article in articles:
            urls.append("https://m.clien.net" + article["href"])
        return (response.status_code, urls)

@article_crawler
def getArticleContent(soup):
    title = soup.find("div", "post_title")
    if title is None: # article has been removed
        return "", ""
    else:
        return title.getText(), soup.find("div", "post_article").getText() # title, content