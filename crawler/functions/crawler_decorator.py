from tqdm import tqdm
from nordvpn_connect import initialize_vpn, rotate_VPN
import utility.constant as constant
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import requests
from bs4 import BeautifulSoup

vpnLock = threading.Lock()
valueLock = threading.Lock()
waiting = False

class NumberWrapper:
    value = 0

def urlCollector(crawler, url, page, article_max, article_num, pbar, headers, vpn):
    url_list = []
    try:
        status_code, urls = crawler(url, page, headers)
        if status_code == 200:
            if len(urls) == 0:
                return url_list
            for u in urls:
                valueLock.acquire(blocking=True)
                if article_num.value < article_max:
                    url_list.append(u)
                    article_num.value += 1
                    pbar.update(1)
                    valueLock.release()
                else:
                    valueLock.release()
                    return url_list
            return url_list
        else: 
            if status_code == constant.TOO_MANY_REQUEST or status_code == constant.SERVICE_UNAVAILABLE: # avoid bot code
                raise ConnectionAbortedError
            else:
                print("Unexpected Status Code! : {0}".format(status_code))
                exit(0)
                
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
        return urlCollector(crawler, url, page, article_max, article_num, pbar, headers, vpn)

def url_crawler(crawler):
    def wrapper(community, name, url, article_max, headers, vpn):
        url_list = []
        article_num = NumberWrapper()
        start = 1
        with tqdm(total=article_max, desc="Collecting URLS for {0}/{1} ".format(community, name) + "=>") as pbar:
            while True:
                with ThreadPoolExecutor(max_workers=constant.MAXTHREAD) as ex:
                    futures = [ex.submit(urlCollector, crawler, url, page, article_max, article_num, pbar, headers, vpn) for page in range(start, start+constant.MAXTHREAD)]
                    for future in futures:
                        result = future.result()
                        url_list.extend(result)

                start += constant.MAXTHREAD
                if article_num.value >= article_max:
                    return url_list
    return wrapper

def article_crawler(crawler):
    def wrapper(article_url, headers):
        response = requests.get(article_url, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            return crawler(soup)
        elif status_code == constant.TOO_MANY_REQUEST or status_code == constant.SERVICE_UNAVAILABLE:
            raise ConnectionAbortedError
        else:
            print("Unexpected Status Code! : {0}".format(status_code))
            exit(0)
    return wrapper