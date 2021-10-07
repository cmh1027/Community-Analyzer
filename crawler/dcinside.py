import requests
from bs4 import BeautifulSoup
import json




request_headers_main = {
    'Host': 'm.dcinside.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-platform': "Windows",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'

}

request_headers_gallery = {
    'Host': 'm.dcinside.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-platform': "Windows",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://m.dcinside.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'

}

prefix = "https://m.dcinside.com"
exclude = ["- dc official App", "\t", "\n"]
############### For fiddler analysis ###############
proxies = {"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}
verify = "FiddlerRoot.pem"
####################################################

def getRankGalleryURLs(soup, rank=1): # 1위 ~ rank위까지 긁어옴
    urls = []
    hotgalls = soup.find("div", "container")
    res = hotgalls.findAll('a')
    for i in range(1, rank+1): # exclude javscript
        urls.append(res[i]["href"])
    return urls

def getGalleryArticleURLs(gallery_url, page=1): # 1~page까지 긁어옴
    urls = []
    for p in range(1, page+1):
        # response = requests.get(gallery_url+"?page="+str(p), headers=request_headers_gallery, proxies=proxies, verify=verify)
        response = requests.get(gallery_url+"?page="+str(p), headers=request_headers_gallery)
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
    response = requests.get(article_url, headers=request_headers_gallery)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("span", "tit") is None: # article has been removed
        return "", ""
    else:
        return soup.find("span", "tit").getText(), soup.find("div", "thum-txt").getText() # title, content

def preprocess(content):
    for e in exclude:
        content = content.replace(e, "")
    content = content.strip()
    return content

if __name__ == "__main__":
    # response = requests.get('https://m.dcinside.com/category/hotgall', headers=request_headers_main, proxies=proxies, verify=verify)
    response = requests.get('https://m.dcinside.com/category/hotgall', headers=request_headers_main)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        galleries = getRankGalleryURLs(soup)
        articleURLs = []
        entire_corpus = []
        for gallery in galleries:
            urls, gallery_name = getGalleryArticleURLs(gallery, page=1)
            corpus = {"name":gallery_name, "content":[]}
            for url in urls:
                title, content = getArticleContent(url)
                title = preprocess(title)
                content = preprocess(content)
                if(title != ""):
                    corpus['content'].append(title)
                if(content != ""):
                    corpus['content'].append(content)
            entire_corpus.append(corpus)
        json.dump(corpus, open("../data/dcinside.json", 'w' ))
        

    else : 
        print(response.status_code)
        assert response.status_code != 200


