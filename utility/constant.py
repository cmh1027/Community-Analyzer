import torch

MAXTHREAD = 4
VPN_COUNTRY = "South Korea"
DEFAULT_HEADER = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-platform': "Windows",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
}
ARTICLE_NUMBER = 100
WEBSITES_ATTIBUTES = {
    "dcinside" : {
        "prefix": "https://m.dcinside.com/board", 
        "host" : "m.dcinside.com",
        "exclude" : ["- dc official App"],
        "hotGalleries": [
            "https://m.dcinside.com/board/baseball_new10",
            "https://m.dcinside.com/board/w_entertainer",
            "https://m.dcinside.com/board/leagueoflegends4",
            "https://m.dcinside.com/board/football_new7",
            "https://m.dcinside.com/board/comic_new3"
        ],
        "hotGalleries_name": [
            "국내야구",
            "여자 연예인",
            "리그 오브 레전드",
            "해외축구",
            "만화"
        ]
    },
    "fmkorea": {
        "prefix": "https://m.fmkorea.com",
        "host" : "m.fmkorea.com",
        "exclude" : ["Video 태그를 지원하지 않는 브라우저입니다."],
        "hotGalleries": [
            "https://www.fmkorea.com/humor",
            "https://www.fmkorea.com/news",
            "https://www.fmkorea.com/lol",
            "https://www.fmkorea.com/paint",
            "https://www.fmkorea.com/fashion"
        ],
        "hotGalleries_name": [
            "유머",
            "정치/시사",
            "리그 오브 레전드",
            "오덕양성소",
            "패션"
        ]
    },
    "pann": {
        "prefix": "https://m.pann.nate.com",
        "host" : "m.pann.nate.com",
        "mainHeader": {},
        "galleryHeader": {},
        "exclude" : [],
        "hotGalleries": [
            "https://m.pann.nate.com/talk/c20001?order=N",
            "https://m.pann.nate.com/talk/c20047?order=N",
            "https://m.pann.nate.com/talk/c20048?order=N",
            "https://m.pann.nate.com/talk/c20050?order=N",
            "https://m.pann.nate.com/talk/c20028?order=N"
        ],
        "hotGalleries_name": [
            "사는 얘기",
            "싱글톡",
            "훈훈한 이야기",
            "TV톡",
            "엔터톡"
        ]
    },
    "clien": {
        "prefix": "https://m.clien.net",
        "host" : "m.clien.net",
        "mainHeader": {},
        "galleryHeader": {},
        "exclude" : [],
        "hotGalleries": [
            "https://m.clien.net/service/group/clien_all",
        ],
        "hotGalleries_name": [
            "톺아보기",
        ]
    },
    "ruliweb": {
        "prefix": "https://m.ruliweb.com",
        "host" : "m.ruliweb.com",
        "exclude" : [],
        "hotGalleries": [
            "https://m.ruliweb.com/community/board/300148",
            "https://m.ruliweb.com/community/board/300143",
            "https://m.ruliweb.com/community/board/300141",
            "https://m.ruliweb.com/community/board/300142",
            "https://m.ruliweb.com/community/board/300147"
        ],
        "hotGalleries_name": [
            "정치유머",
            "유머",
            "자유",
            "질문",
            "고민상담"
        ]
    },
    "theqoo": {
        "prefix": "https://theqoo.net",
        "host" : "theqoo.net",
        "exclude" : [],
        "hotGalleries": [
            "https://theqoo.net/square",
            "https://theqoo.net/beauty",
            "https://theqoo.net/ktalk",
            "https://theqoo.net/dyb",
            "https://theqoo.net/japan"
        ],
        "hotGalleries_name": [
            "스퀘어",
            "뷰티",
            "케이돌토크",
            "드영배",
            "재팬"
        ]
    },
}
BERT_VOCAB_SIZE = 8002
FORMATS = ["bert", "okt_adjv", "okt_noun"]
WEIGHT = torch.tensor([1.0, 1.0, 1.0])
DOCVEC_SIZE = 200
EMBED_SIZE = DOCVEC_SIZE*len(FORMATS)
BATCH_SIZE = 1000
DOC2VEC_EPOCH = 1000
DECODER_EPOCH = 1000
SENTENCE_MAXLEN = 50
BERT_UNDERLINE = "▁"
RANDOM_CHOICE = 5
SOFTMAX_TEMPERATURE = 1
DECODER_TOKENIZERS = ["Bert", "Okt"]
DECODER_TOKENIZER = DECODER_TOKENIZERS[0]
SENTENCE_NORMARLIZE = True
class BertToken:
    UNK_TOKEN = "[UNK]"
    PAD_TOKEN = "[PAD]"
    END_TOKEN = "[END]"
    UNK_TOKEN_IND = 0
    PAD_TOKEN_IND = 1
    END_TOKEN_IND = 2