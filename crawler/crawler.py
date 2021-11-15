import json
import sys, os
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utility.preprocess import sentencePreprocess
import utility.constant as constant
from concurrent.futures import ThreadPoolExecutor, as_completed
from functions import dcinside, pann, ruliweb, theqoo, clien #, fmkorea
############### For fiddler analysis ###############
# proxies = {"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}
# verify = "FiddlerRoot.pem"
####################################################
communityList = [('dcinside', dcinside), ('pann', pann), ('ruliweb', ruliweb), ('clien', clien), ('theqoo', theqoo)]
# communityList = [('dcinside', dcinside), ('pann', pann), ('ruliweb', ruliweb), ('clien', clien), ('theqoo', theqoo), ('fmkorea', fmkorea)]

def threading(url, corpus, module):
    title, content = module.getArticleContent(url)
    corpus.append(title)
    corpus.append(content)

if __name__ == "__main__":
    for i, (community, module) in enumerate(communityList):
        headers = constant.DEFAULT_HEADER
        headers.update({"Host": constant.WEBSITES_ATTIBUTES[community]['host']})
        galleries = constant.WEBSITES_ATTIBUTES[community]["hotGalleries"]
        entire_corpus = []
        for j, gallery in enumerate(galleries):
            urls = module.getGalleryArticleURLs(gallery, article_max=int(constant.ARTICLE_NUMBER / len(constant.WEBSITES_ATTIBUTES[community]["hotGalleries"])))
            gallery_name = constant.WEBSITES_ATTIBUTES[community]["hotGalleries_name"][j]
            corpus = []
            with tqdm(total=len(urls), desc="Crawling... : " + community + " / " + gallery_name + " =>") as pbar:
                with ThreadPoolExecutor(max_workers=constant.MAXTHREAD) as ex:
                    futures = [ex.submit(threading, url, corpus, module) for url in urls]
                    for future in as_completed(futures):
                        result = future.result()
                        pbar.update(1)
            preprocessed_corpus = []
            for i, sentence in tqdm(enumerate(corpus), desc="Sentence Preprocessing..."):
                preprocessed = sentencePreprocess(sentence, exclude=constant.WEBSITES_ATTIBUTES[community]["exclude"])
                if preprocessed != "":
                    preprocessed_corpus.append(preprocessed)
            entire_corpus.append({"name": community + "/" + gallery_name, "content":preprocessed_corpus})
        json.dump(entire_corpus, open(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "data/" + community + ".json"), 'w' ))