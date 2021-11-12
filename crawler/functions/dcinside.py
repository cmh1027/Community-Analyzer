import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['dcinside']['host']})

def getRankGalleryURLs(soup, rank=5): # 1위 ~ rank위까지 긁어옴
    urls = []
    hotgalls = soup.find("div", "container")
    res = hotgalls.findAll('a')
    for i in range(1, rank+1): # exclude javscript
        # print(res[i]["href"])
        urls.append(res[i]["href"])
    return urls

def getGalleryArticleURLs(gallery_url, page=1): # 1~page까지 긁어옴
    urls = []
    for p in range(1, page+1):
        # response = requests.get(gallery_url+"?page="+str(p), headers=request_headers_gallery, proxies=proxies, verify=verify)
        response = requests.get(gallery_url+"?page="+str(p), headers=headers)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            if p == 1:
                gallery_name = soup.find("h3", "gall-tit").findChild("a").getText().strip()
            articles = soup.find("ul", "gall-detail-lst")
            for article in articles.findAll('a', 'lt'):
                url = article["href"]
                urls.append(url)
        else: 
            print(response.status_code)
            assert response.status_code != 200
    return urls, gallery_name

def getArticleContent(article_url):
    # response = requests.get(article_url, headers=request_headers_gallery, proxies=proxies, verify=verify)
    response = requests.get(article_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("span", "tit") is None: # article has been removed
        return "", ""
    else:
        return soup.find("span", "tit").getText(), soup.find("div", "thum-txt").getText() # title, content