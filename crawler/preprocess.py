import re
def preprocessing(content, exclude=[]):
    for e in exclude:
        content = content.replace(e, "")
    content.replace("\n", " ")
    hangul = re.compile('[^ ㄱ-ㅣ가-힣+]') 
    content = hangul.sub('', content)
    content = content.strip()
    if content.count(" ") == 0:
        content = ""
    return content