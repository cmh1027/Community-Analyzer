import torch

MAXTHREAD = 4

DEFAULT_HEADER = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-platform': "Windows",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
}

WEBSITES_ATTIBUTES = {
    "dcinside" : {
        "prefix": "https://m.dcinside.com/category/hotgall", 
        "host" : "m.dcinside.com",
        "rank" : 1,
        "page" : 1,
        "exclude" : ["- dc official App"]
    },
    "fmkorea": {
        "prefix": "https://m.fmkorea.com/",
        "host" : "m.fmkorea.com",
        "rank": 6,
        "page": 1,
        "exclude" : ["Video 태그를 지원하지 않는 브라우저입니다."]
    },
    "pann": {
        "prefix": "https://pann.nate.com/",
        "host" : "m.fmkorea.com",
        "mainHeader": {},
        "galleryHeader": {},
        "rank": 0,
        "page": 10,
        "exclude" : [],
        "hotGalleries": [
            "https://pann.nate.com/talk/c20001",
            "https://pann.nate.com/talk/c20047",
            "https://pann.nate.com/talk/c20048",
            "https://pann.nate.com/talk/c20050",
            "https://pann.nate.com/talk/c20028"
        ]
    },
    "": {
        "prefix": "",
        "mainHeader": {},
        "galleryHeader": {},
        "rank": 0,
        "page": 10,
        "exclude" : []
    },
    "": {
        "prefix": "",
        "mainHeader": {},
        "galleryHeader": {},
        "rank": 0,
        "page": 10,
        "exclude" : []
    },
}
BERT_VOCAB_SIZE = 8002
UNK_TOKEN = 0
PAD_TOKEN = 1
END_TOKEN = 2
FORMATS = ["bert", "okt_adjv", "okt_noun"]
DOCVEC_SIZE = 200
EMBED_SIZE = DOCVEC_SIZE*len(FORMATS)
BATCH_SIZE = 100
EPOCH = 1000
WEIGHT = torch.tensor([1.0, 1.0, 1.0])
SENTENCE_MAXLEN = 50
BERT_UNDERLINE = "▁"
RANDOM_CHOICE = 5
SOFTMAX_TEMPERATURE = 1