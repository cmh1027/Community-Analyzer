from tqdm import tqdm
from nordvpn_connect import initialize_vpn, rotate_VPN
import utility.constant as constant
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

vpnLock = threading.Lock()
valueLock = threading.Lock()
waiting = False

class NumberWrapper:
    value = 0

def urlCollector(crawler, url, page, article_max, article_num, pbar, vpn):
    url_list = []
    try:
        status_code, urls = crawler(url, page)
        if status_code == 200:
            if len(urls) == 0:
                return url_list
            for u in urls:
                vpnLock.acquire(blocking=True)
                if article_num.value < article_max:
                    url_list.append(u)
                    article_num.value += 1
                    pbar.update(1)
                    vpnLock.release()
                else:
                    vpnLock.release()
                    return url_list
            return url_list
        else: 
            if status_code == 429: # avoid bot code
                raise ConnectionAbortedError
            else:
                assert status_code
    except ConnectionAbortedError:
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
        return urlCollector(crawler, url, page, article_max, article_num, pbar, vpn)

def crawler_decorator(crawler):
    def wrapper(community, name, url, article_max, vpn, *args, **kwargs):
        url_list = []
        article_num = NumberWrapper()
        start = 1
        with tqdm(total=article_max, desc="Collecting URLS for {0}/{1} ".format(community, name) + "=>") as pbar:
            while True:
                with ThreadPoolExecutor(max_workers=constant.MAXTHREAD) as ex:
                    futures = [ex.submit(urlCollector, crawler, url, page, article_max, article_num, pbar, vpn) for page in range(start, start+constant.MAXTHREAD)]
                    for future in futures:
                        url_list.extend(future.result())
                start += constant.MAXTHREAD
                if article_num.value >= article_max:
                    return url_list
    return wrapper