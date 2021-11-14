import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utility.constant as constant

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

option = webdriver.ChromeOptions()
option.add_argument('--kiosk-printing')
option.add_argument('--log-level=3') 
option.headless = True 
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_options=option, executable_path='E:\GitHub\Community-Analyzer\crawler\chromedriver.exe') # 이거 로컬환경 맞게 세팅해야함

headers = constant.DEFAULT_HEADER
headers.update({"Host": constant.WEBSITES_ATTIBUTES['theqoo']['host']})



def getGalleryArticleURLs(gallery_url, page=1): # 1~page까지 긁어옴
    urls = []
    
    gallery_cate = gallery_url[19:]
    # print(gallery_cate)
    
    for p in range(1, page+1):
        
        driver.get("https://theqoo.net/index.php?mid=" + gallery_cate+"&filter_mode=normal&page="+str(p))
        gallery_name = ''
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find("tbody", "hide_notice").findAll("tr", {'class': None})        
        
        for article in articles:
            url = article.find("a")["href"]
            urls.append("https://theqoo.net" + url)
    return urls, gallery_name

def getArticleContent(article_url):
    driver.get(article_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    if soup.find("span", "title") is None: # article has been removed
        return "", ""
    else:
        return soup.find("span", "title").getText(), soup.find("article").getText() # title, content