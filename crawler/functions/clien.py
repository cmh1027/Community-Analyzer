import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['clien']['host']})


# def getRankGalleryURLs(soup, rank=5): # 1위 ~ rank위까지 긁어옴
#     urls = []
#     hotgalls = soup.find("div", "container")
#     res = hotgalls.findAll('a')
#     for i in range(1, rank+1): # exclude javscript
#         # print(res[i]["href"])
#         urls.append(res[i]["href"])
#     return urls

def getGalleryArticleURLs(gallery_url, page=1): # 1~page까지 긁어옴
    urls = []
    
    for p in range(0, page):
        response = requests.get(gallery_url+"?od=T31&category=0&po="+str(p), headers=headers)
        
        gallery_name = ''
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            articles = soup.findAll("a", "list_subject")
            for i, article in enumerate(articles):
                if i == 0 : 
                    continue
                url = article["href"]
                urls.append("https://m.clien.net" + url)
        else: 
            print(response.status_code)
            assert response.status_code != 200
    return urls, gallery_name

def getArticleContent(article_url):
    # response = requests.get(article_url, headers=request_headers_gallery, proxies=proxies, verify=verify)
    response = requests.get(article_url, headers=headers)
    # print(response)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    # print(article_url)
    # print(soup.find("div", "post_title").find("span").getText())
    if soup.find("div", "post_title") is None: # article has been removed
        return "", ""
    else:
        return soup.find("div", "post_title").getText(), soup.find("div", "post_article").getText() # title, content