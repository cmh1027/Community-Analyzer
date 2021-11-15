import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['theqoo']['host']})

def getGalleryArticleURLs(gallery_url, page=1): # 1~page까지 긁어옴
    urls = []
    prefix = constant.WEBSITES_ATTIBUTES["theqoo"]["prefix"]
    for p in range(1, page+1):
        category = gallery_url[len(prefix)+1:]
        # response = requests.get("https://theqoo.net/index.php?mid={0}&page={1}".format(category, p), headers=headers, proxies=proxies, verify=verify)
        response = requests.get("https://theqoo.net/index.php?mid={0}&page={1}".format(category, p), headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            for url in soup.find('ul', 'list').findAll('a'):
                if "#comment" not in url["href"]:
                    urls.append(prefix+url["href"])
        else: 
            print(response.status_code)
            assert response.status_code != 200
    return urls

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