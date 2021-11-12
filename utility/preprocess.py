import re
from tqdm import tqdm

def sentencePreprocess(content, exclude=[]):
    for e in exclude:
        content = content.replace(e, "")
    content.replace("\n", ".")
    content = re.compile(r'[^ .,?!ㄱ-ㅣ가-힣]').sub('', content) # 한글, 문장부호만
    startreg = re.search(r"[ㄱ-ㅣ가-힣]", content)
    if startreg is None:
        content = ""
    else:
        content = content[startreg.start():] # 첫 문장은 한글로 시작
    content = re.compile(r'([.,?! ])\1+').sub(r'\1', content) # 연속된 문장부호 제거
    content = content.strip()
    return content

def sentencesBertTokenize(sentences, tokenizer, vocab, name=""):
    sentences_tokenized = []
    sentences_tokenized_ind = []
    for sentence in tqdm(sentences, desc=name+" BERT-tokenizing..."):
        tokens = tokenizer(sentence)
        sentences_tokenized.append(tokens)
        sentences_tokenized_ind.append(list(map(lambda s: vocab[s], tokens)))
    return sentences_tokenized, sentences_tokenized_ind

def sentencesOktTokenize(sentences, tokenizer, name=""):
    sentences_tokenized = []
    for sentence in tqdm(sentences, desc=name+" Okt-tokenizing..."):
        tokens = tokenizer.pos(sentence, join=True, norm=True)
        sentences_tokenized.append(tokens)
    return sentences_tokenized

def pickOnlyNouns(sentences):
    new_sentences = []
    for sentence in sentences:
        new_sentence = []
        for word in sentence:
            if "/Noun" in word:
                new_sentence.append(word.replace("/Noun", ""))
        if len(new_sentence) > 0:
            new_sentences.append(new_sentence)
    return new_sentences 

def pickOnlyAdjsVerb(sentences):
    new_sentences = []
    for sentence in sentences:
        new_sentence = []
        for word in sentence:
            if "/Verb" in word or "/Adjective" in word:
                new_sentence.append(word.replace("/Verb", "").replace("/Adjective", ""))
        if len(new_sentence) > 0:
            new_sentences.append(new_sentence)
    return new_sentences 

# def gen_attention_mask(token_ids, valid_length):
#     attention_mask = torch.zeros_like(token_ids)
#     attention_mask[:valid_length] = 1
#     return attention_mask.float()

# def sentences2embed(sentences, bertmodel, transform):
#     sentences_embedded = []
#     for sentence in sentences:
#         token_ids, valid_length, segment_ids = transform(sentence)
#         token_ids = torch.tensor(token_ids).view(1, -1)
#         valid_length = torch.tensor(valid_length).view(1, -1)
#         segment_ids = torch.tensor(segment_ids).view(1, -1)
#         attention_mask = gen_attention_mask(token_ids, valid_length)
#         _, embedding = bertmodel(input_ids = token_ids, token_type_ids = segment_ids, attention_mask = attention_mask.float())
#         sentences_embedded.append(embedding.tolist())
#     return sentences_embedded 