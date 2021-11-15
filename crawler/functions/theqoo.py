import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from functions.crawler_decorator import url_crawler, article_crawler
import utility.constant as constant

@url_crawler
def getGalleryArticleURLs(gallery_url, page, headers): # article_max 개의 게시글을 긁어옴
    urls = []
    prefix=constant.WEBSITES_ATTIBUTES["theqoo"]["prefix"]
    category = gallery_url[len(prefix)+1:]
    response = requests.get("https://theqoo.net/index.php?mid={0}&page={1}".format(category, page), headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        article_list = soup.find('ul', 'list').findAll('a')
        urls = []
        for article in article_list:
            if "#comment" not in article["href"]:
                urls.append(prefix+article["href"])
        return (response.status_code, urls)

@article_crawler
def getArticleContent(soup):
    title = soup.find("h3")
    if title is None: # article has been removed
        return "", ""
    else:
        return title.find("h3").getText(), soup.find("div", "read-body").getText() # title, content