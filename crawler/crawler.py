import requests
from bs4 import BeautifulSoup
import json
import sys, os
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utility.preprocess import rawPreprocess
import utility.constant as constant
from concurrent.futures import ThreadPoolExecutor, as_completed

from functions import dcinside, fmkorea

communityList = ['dcinside', 'fmkorea', 'pann', 'ruliweb', 'theqoo']
communityModules = [dcinside, fmkorea]
############### For fiddler analysis ###############
proxies = {"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}
verify = "FiddlerRoot.pem"
####################################################

if __name__ == "__main__":
    try: 
        # response = requests.get('https://m.dcinside.com/category/hotgall', headers=request_headers_main, proxies=proxies, verify=verify)
        for i, community in enumerate(communityList) :
            
            headers = constant.DEFAULT_HEADER
            headers.update({"Host": constant.WEBSITES_ATTIBUTES[community]['host']})

            # print(constant.WEBSITES_ATTIBUTES[community]["prefix"])
            # response = requests.get('https://m.dcinside.com/category/hotgall', headers=constant.DEFAULT_HEADER.update({"Host": constant.WEBSITES_ATTIBUTES['dcinside']['host']}))
            response = requests.get(constant.WEBSITES_ATTIBUTES[community]["prefix"], headers=headers)
            
            print(constant.WEBSITES_ATTIBUTES[community]["prefix"])
            print(headers)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                galleries = communityModules[i].getRankGalleryURLs(soup, constant.WEBSITES_ATTIBUTES[community]["rank"])
                print(galleries)
                articleURLs = []
                entire_corpus = []
                for gallery in galleries:
                    urls, gallery_name = communityModules[i].getGalleryArticleURLs(gallery, page=constant.WEBSITES_ATTIBUTES[community]["page"])
                    print(urls)
                    print(galleries)
                    corpus = {"name": community + "/" + gallery_name, "content":[]}
                    # print(corpus)
                    with tqdm(total=len(urls), desc="Processing : " + community + " / " + gallery_name + " =>") as pbar:
                        with ThreadPoolExecutor(max_workers=constant.MAXTHREAD) as ex:
                            futures = [ex.submit(communityModules[i].threading, url, corpus) for url in urls]
                            for future in as_completed(futures):
                                result = future.result()
                                pbar.update(1)
                    entire_corpus.append(corpus)
                json.dump(entire_corpus, open(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "data/" + community + ".json"), 'w' ))

        else : 
            print(response.status_code)
            assert response.status_code != 200
    except KeyboardInterrupt:
        pass
