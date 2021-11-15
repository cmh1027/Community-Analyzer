import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant
from functions.crawler_decorator import url_crawler, article_crawler

@url_crawler
def getGalleryArticleURLs(gallery_url, page, headers): # article_max 개의 게시글을 긁어옴
    urls = []
    response = requests.get(gallery_url+"?page="+str(page), headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find("tbody")
        for div in soup.find_all("tr", {'class':'table_body notice inside screen_out'}): 
            div.decompose() # 공지글 제외
        for div in soup.find_all("tr", {'class':'table_body best'}): 
            div.decompose() # best글 제외 
        for div in soup.find_all("tr", {'class':'table_body list_inner'}): 
            div.decompose() # 광고글 제외
        article_list = articles.findAll('a', 'subject_link deco')
        urls = []
        for article in article_list:
            url = article["href"]
            urls.append(url)
    return (response.status_code, urls)

@article_crawler
def getArticleContent(soup):
    title = soup.find("span", "subject_inner_text")
    if title is None: # article has been removed
        return "", ""
    else:
        return title.getText(), soup.find("article").getText() # title, content