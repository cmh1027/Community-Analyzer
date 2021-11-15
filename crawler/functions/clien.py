import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant
from tqdm import tqdm
from nordvpn_connect import initialize_vpn, rotate_VPN
from functions.crawler_decorator import crawler_decorator

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['clien']['host']})

@crawler_decorator
def getGalleryArticleURLs(gallery_url, page): # article_max 개의 게시글을 긁어옴
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

def getArticleContent(article_url):
    response = requests.get(article_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("div", "post_title") is None: # article has been removed
        return "", ""
    else:
        return soup.find("div", "post_title").getText(), soup.find("div", "post_article").getText() # title, content