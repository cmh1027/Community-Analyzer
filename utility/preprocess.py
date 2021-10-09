import re
from .stopwords import remove_stopwords
from konlpy.tag import Okt

def rawPreprocess(content, exclude=[]):
    for e in exclude:
        content = content.replace(e, "")
    content.replace("\n", " ")
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]')  # 한글만
    content = hangul.sub('', content)
    content = content.strip()
    if content.count(" ") == 0:
        content = ""
    return content

def sentenceProprocess(sentence):
    okt = Okt()
    # input : string
    return remove_stopwords(okt.morphs(okt.normalize(sentence)))