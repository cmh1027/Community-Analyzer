import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant
from functions.crawler_decorator import crawler_decorator
headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['fmkorea']['host']})

@crawler_decorator
def getGalleryArticleURLs(gallery_url, page): # 1~page까지 긁어옴
    urls = []
    response = requests.get(gallery_url+"?page="+str(page), headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find("ol", "bd_lst")
        article_list = articles.findAll('li', 'clear')
        urls = []
        for article in article_list:
            if len(article["class"]) != 1 : # 공지, 인기글 제외
                continue
            url = article.findChild("a")["href"]
            urls.append(constant.WEBSITES_ATTIBUTES['fmkorea']['prefix'] + url)                       
    return (response.status_code, urls)

def getArticleContent(article_url):
    # response = requests.get(article_url, headers=request_headers_gallery, proxies=proxies, verify=verify)
    response = requests.get(article_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("span", "np_18px_span") is None: # article has been removed
        return "", ""
    else:
        return soup.find("span", "np_18px_span").getText(), soup.find("article").getText() # title, content