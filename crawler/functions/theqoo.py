import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['theqoo']['host']})

def getGalleryArticleURLs(gallery_url, article_max=1): # article_max 개의 게시글을 긁어옴
    urls = []
    page = 1
    article_num = 0
    prefix = constant.WEBSITES_ATTIBUTES["theqoo"]["prefix"]
    while True:
        category = gallery_url[len(prefix)+1:]
        response = requests.get("https://theqoo.net/index.php?mid={0}&page={1}".format(category, page), headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            article_list = soup.find('ul', 'list').findAll('a')
            if len(article_list) == 0:
                return urls
            for url in article_list:
                if "#comment" not in url["href"]:
                    urls.append(prefix+url["href"])
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
    title = soup.find("h3")
    content = soup.find("div", "read-body")
    if title is None: # article has been removed
        return "", ""
    else:
        return title.getText(), content.getText() # title, content