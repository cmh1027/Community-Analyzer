import re
from tqdm import tqdm
# from kobert.pytorch_kobert import get_pytorch_kobert_model

def rawPreprocess(content, exclude=[]):
    for e in exclude:
        content = content.replace(e, "")
    content.replace("\n", " ")
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]')  # 한글만
    content = hangul.sub('', content)
    content = content.strip()
    return content

def sentencesBertTokenize(sentences, tokenizer, name=""):
    sentences_tokenized = []
    for sentence in tqdm(sentences, desc=name+" BERT-tokenizing..."):
        tokens = tokenizer(sentence)
        sentences_tokenized.append(tokens)
    return sentences_tokenized

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
                new_sentence.append(word.replace("/Verb", "").replace("Adjective", ""))
        if len(new_sentence) > 0:
            new_sentences.append(new_sentence)
    return new_sentences 

# bertmodel, vocab = get_pytorch_kobert_model()
# tokenizer = get_tokenizer()
# tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
# max_len = 64
# transform = nlp.data.BERTSentenceTransform(tok, max_seq_length=max_len, pad=True, pair=False)

# def gen_attention_mask(token_ids, valid_length):
#     attention_mask = torch.zeros_like(token_ids)
#     attention_mask[:valid_length] = 1
#     return attention_mask.float()

# def sentencesPreprocess(sentences):
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

