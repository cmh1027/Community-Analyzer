import json
import sys, os
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utility.preprocess import sentencePreprocess
import utility.constant as constant
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import argparse
from nordvpn_connect import initialize_vpn, rotate_VPN, close_vpn_connection
from functions import dcinside, pann, ruliweb, theqoo, clien, fmkorea
import requests
import time
############### For fiddler analysis ###############
# proxies = {"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}
# verify = "FiddlerRoot.pem"
####################################################
communityList_VPN = [('clien', clien)]
# communityList_VPN = [('clien', clien), ('fmkorea', fmkorea)]
communityList_VPN_strict = ['fmkorea']
communityList_NoVPN = [('dcinside', dcinside), ('pann', pann), ('ruliweb', ruliweb), ('theqoo', theqoo)]

class VPNWrapper:
    vpn = None

vpnLock = threading.Lock() 
waiting = False
vpn = VPNWrapper()

def articleRetriever(url, module, pbar, headers, vpn):
    def corpus_append(url):
        title, content = module.getArticleContent(url, headers)
        pbar.update(1)
        result = []
        if title != "":
            result.append(title)
        if content != "":
            result.append(content)
        return result     
    try:
        return corpus_append(url)
    except (ConnectionAbortedError, requests.exceptions.ConnectionError):
        global waiting
        if vpnLock.acquire(blocking=False) is True:
            waiting = True
            print("\r", end="")
            if vpn.vpn is None:
                vpn.vpn = initialize_vpn(constant.VPN_COUNTRY)
            else:
                rotate_VPN(vpn.vpn)
            waiting = False
            vpnLock.release()
        else:
            while waiting is True:
                pass
        return articleRetriever(url, module, pbar, headers, vpn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--vpn', type=int)
    args = parser.parse_args()
    if args.vpn != 0 and args.vpn is not None:
        vpn.vpn = initialize_vpn(constant.VPN_COUNTRY)  # starts nordvpn and stuff
        rotate_VPN(vpn.vpn)  # actually connect to server
        communityList = communityList_VPN
    else:
        communityList = communityList_NoVPN
    try:
        for i, (community, module) in enumerate(communityList):
            headers = constant.DEFAULT_HEADER
            headers.update({"Host": constant.WEBSITES_ATTIBUTES[community]['host']})
            galleries = constant.WEBSITES_ATTIBUTES[community]["hotGalleries"]
            entire_corpus = []
            for j, gallery_url in enumerate(galleries):
                gallery_name = constant.WEBSITES_ATTIBUTES[community]["hotGalleries_name"][j]
                urls = module.getGalleryArticleURLs(community, gallery_name, gallery_url, 
                            int(constant.ARTICLE_NUMBER / len(constant.WEBSITES_ATTIBUTES[community]["hotGalleries"])), headers, vpn)
                corpus = []
                with tqdm(total=len(urls), desc="Crawling " + community + " / " + gallery_name + " =>") as pbar:
                    with ThreadPoolExecutor(max_workers=constant.MAXTHREAD) as ex:
                        futures = [ex.submit(articleRetriever, url, module, pbar, headers, vpn) for url in urls]
                        for future in as_completed(futures):
                            corpus.extend(future.result())
                            if community in communityList_VPN_strict:
                                time.sleep(1)
                preprocessed_corpus = []
                with tqdm(total=len(corpus), desc="Sentence Preprocessing...") as pbar:
                    with ThreadPoolExecutor(max_workers=constant.MAXTHREAD) as ex:
                        futures = [ex.submit(sentencePreprocess, sentence, exclude=constant.WEBSITES_ATTIBUTES[community]["exclude"]) for sentence in corpus]
                        for future in as_completed(futures):
                            result = future.result()
                            if result != "":
                                preprocessed_corpus.append()
                            pbar.update(1)
                entire_corpus.append({"name": community + "/" + gallery_name, "content":preprocessed_corpus})
            json.dump(entire_corpus, open(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "data/" + community + ".json"), 'w' ))
    finally:
        if vpn.vpn is not None:
            close_vpn_connection(vpn.vpn)