import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant
from functions.crawler_decorator import crawler_decorator
headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['dcinside']['host']})

@crawler_decorator
def getGalleryArticleURLs(gallery_url, page): # article_max 개의 게시글을 긁어옴
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

def getArticleContent(article_url):
    # response = requests.get(article_url, headers=request_headers_gallery, proxies=proxies, verify=verify)
    response = requests.get(article_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("span", "tit") is None: # article has been removed
        return "", ""
    else:
        return soup.find("span", "tit").getText(), soup.find("div", "thum-txt").getText() # title, content