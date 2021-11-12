import requests
from bs4 import BeautifulSoup
import json
import sys, os
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utility.preprocess import rawPreprocess
import utility.constant as constant
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def getGalleryArticleURLs(gallery_url, page=1): # 1~page까지 긁어옴
    urls = []
    
    for p in range(1, page+1):
        response = requests.get(gallery_url+"?page="+str(p), headers=headers)
        gallery_name = ''
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
            
            
            
            for article in articles.findAll('a', 'subject_link deco'):
                url = article["href"]
                urls.append(url)
                        
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
    if soup.find("span", "subject_inner_text") is None: # article has been removed
        return "", ""
    else:
        return soup.find("span", "subject_inner_text").getText(), soup.find("article").getText() # title, content

def threading(url, corpus):
    title, content = getArticleContent(url)
    # print('title: ' + title + " / content: " + content)
    title = rawPreprocess(title, exclude=constant.WEBSITES_ATTIBUTES["ruliweb"]["exclude"])
    content = rawPreprocess(content, exclude=constant.WEBSITES_ATTIBUTES["ruliweb"]["exclude"])
    if(title != ""):
        corpus['content'].append(title)
    if(content != ""):
        corpus['content'].append(content)
