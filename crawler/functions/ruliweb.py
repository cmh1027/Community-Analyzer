import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['ruliweb']['host']})


# def getRankGalleryURLs(soup, rank=5): # 1위 ~ rank위까지 긁어옴
#     urls = []
#     hotgalls = soup.find("div", "container")
#     res = hotgalls.findAll('a')
#     for i in range(1, rank+1): # exclude javscript
#         # print(res[i]["href"])
#         urls.append(res[i]["href"])
#     return urls

def getGalleryArticleURLs(gallery_url, article_max=1): # article_max 개의 게시글을 긁어옴
    urls = []
    page = 1
    article_num = 0
    while True:
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
            if len(article_list) == 0:
                return urls
            for article in article_list:
                url = article["href"]
                urls.append(url)     
                article_num += 1
                if article_num >= article_max:
                    return urls  
        else: 
            print(response.status_code)
            assert response.status_code != 200
        page += 1

def getArticleContent(article_url):
    # response = requests.get(article_url, headers=request_headers_gallery, proxies=proxies, verify=verify)
    response = requests.get(article_url, headers=headers)
    # print(response)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    if soup.find("span", "subject_inner_text") is None: # article has been removed
        return "", ""
    else:
        return soup.find("span", "subject_inner_text").getText(), soup.find("article").getText() # title, content