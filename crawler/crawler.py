import requests
from bs4 import BeautifulSoup
import json
import sys, os
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utility.preprocess import sentencePreprocess
import utility.constant as constant
from concurrent.futures import ThreadPoolExecutor, as_completed
from functions import dcinside, pann, ruliweb, theqoo, fmkorea
from konlpy.tag import Okt 
############### For fiddler analysis ###############
proxies = {"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}
verify = "FiddlerRoot.pem"
####################################################
communityList = [('dcinside', dcinside)]
# communityList = [('dcinside', dcinside), ('pann', pann), ('ruliweb', ruliweb), ('theqoo', theqoo), ('fmkorea', fmkorea)]

def threading(url, corpus, module):
    title, content = module.getArticleContent(url)
    corpus.append(title)
    corpus.append(content)

if __name__ == "__main__":
    if constant.SENTENCE_NORMARLIZE is True:
        okt = Okt()
    try: 
        for i, (community, module) in enumerate(communityList):
            headers = constant.DEFAULT_HEADER
            headers.update({"Host": constant.WEBSITES_ATTIBUTES[community]['host']})
            response = requests.get(constant.WEBSITES_ATTIBUTES[community]["prefix"], headers=headers)
            # print(response)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                if community in ['pann', 'ruliweb', 'theqoo']:
                    galleries = constant.WEBSITES_ATTIBUTES[community]["hotGalleries"]
                # elif(community == 'theqoo'):
                #     galleries = constant.WEBSITES_ATTIBUTES[community]["hotGalleries"]    
                else:    
                    galleries = module.getRankGalleryURLs(soup, constant.WEBSITES_ATTIBUTES[community]["rank"])
                # print(galleries)    
                entire_corpus = []
                for j, gallery in enumerate(galleries):
                #     print('start crawling: ' + community)
                    urls, gallery_name = module.getGalleryArticleURLs(gallery, page=constant.WEBSITES_ATTIBUTES[community]["page"])
                    if(community == 'pann'):
                        gallery_name = constant.WEBSITES_ATTIBUTES[community]["hotGalleries_name"][j]
                    elif(community == 'ruliweb'):
                        gallery_name = constant.WEBSITES_ATTIBUTES[community]["hotGalleries_name"][j]
                    # elif(community == 'theqoo'):
                    #     gallery_name = constant.WEBSITES_ATTIBUTES[community]["hotGalleries_name"][j]
                    corpus = []
                    # print(gallery_name)
                    # print(urls)
                    with tqdm(total=len(urls), desc="Crawling... : " + community + " / " + gallery_name + " =>") as pbar:
                        with ThreadPoolExecutor(max_workers=constant.MAXTHREAD) as ex:
                            futures = [ex.submit(threading, url, corpus, module) for url in urls]
                            for future in as_completed(futures):
                                result = future.result()
                                pbar.update(1)
                    preprocessed_corpus = []
                    for i, sentence in tqdm(enumerate(corpus), desc="Sentence Preprocessing..."):
                        preprocessed = sentencePreprocess(sentence, exclude=constant.WEBSITES_ATTIBUTES[community]["exclude"])
                        if constant.SENTENCE_NORMARLIZE is True:
                            preprocessed = okt.normalize(preprocessed)
                        if preprocessed != "":
                            preprocessed_corpus.append(preprocessed)
                    entire_corpus.append({"name": community + "/" + gallery_name, "content":preprocessed_corpus})
                json.dump(entire_corpus, open(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "data/" + community + ".json"), 'w' ))
            else : 
                print(response.status_code)
                assert response.status_code != 200
    except KeyboardInterrupt: # Ctrl + c로 중단 가능
        pass

