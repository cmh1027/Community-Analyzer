import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from functions.crawler_decorator import url_crawler, article_crawler
import requests
from bs4 import BeautifulSoup
import utility.constant as constant

@url_crawler
def getGalleryArticleURLs(gallery_url, page, headers): # article_max 개의 게시글을 긁어옴
    response = requests.get(gallery_url+"?page="+str(page), headers=headers)
    urls = []
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find("ul", "gall-detail-lst")
        article_list = articles.findAll('a', 'lt')
        for article in article_list:
            urls.append(article["href"])
    return (response.status_code, urls)

@article_crawler
def getArticleContent(soup):
    title = soup.find("span", "tit")
    if title is None: # article has been removed
        return "", ""
    else:
        return title.getText(), soup.find("div", "thum-txt").getText() # title, content