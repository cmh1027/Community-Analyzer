import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['fmkorea']['host']})

def getRankGalleryURLs(soup, rank=5): # 1위 ~ rank위까지 긁어옴
    urls = []
    hotBoards = soup.find("nav", "fmkorea_m_navi")
    res = hotBoards.findAll('a')
    for i in range(1, rank+1): # exclude javscript
        if res[i]["href"] == "hotdeal" :
            continue
        urls.append(constant.WEBSITES_ATTIBUTES['fmkorea']['prefix'] + res[i]["href"])
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
                gallery_name = soup.find("h1", "ngeb").findChild("a").getText().strip()
                #print(gallery_name)
                
            articles = soup.find("ol", "bd_lst")
            for article in articles.findAll('li', 'clear'):
                if len(article["class"]) != 1 : # 공지, 인기글 제외
                    continue
                url = article.findChild("a")["href"]
                urls.append(constant.WEBSITES_ATTIBUTES['fmkorea']['prefix'] + url)
            #print(urls)
        else: 
            #print(response.status_code)
            assert response.status_code != 200
    return urls, gallery_name

def getArticleContent(article_url):
    # response = requests.get(article_url, headers=request_headers_gallery, proxies=proxies, verify=verify)
    response = requests.get(article_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("span", "np_18px_span") is None: # article has been removed
        return "", ""
    else:
        return soup.find("span", "np_18px_span").getText(), soup.find("article").getText() # title, content