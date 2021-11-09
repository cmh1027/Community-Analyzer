import json
import os
from utility.preprocess import sentencesBertTokenize, sentencesOktTokenize, pickOnlyNouns, pickOnlyAdjsVerb#, sentences2embed
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
from konlpy.tag import Okt
import constant
import gluonnlp as nlp

if __name__ == "__main__":
    bertmodel, vocab = get_pytorch_kobert_model()
    tokenizer = get_tokenizer()
    tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
    # transform = nlp.data.BERTSentenceTransform(tok, max_seq_length = 64, pad=True, pair=False)
    okt = Okt()
    for website in constant.WEBSITES:
        data = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/" + website + ".json"), 'r'))
        data_bert_processed = []
        data_bert_processed_ind = []
        data_okt_noun_processed = []
        data_okt_adjv_processed = []
        ############### BERT Tokenizer ###############
        for board in data:
            bert_tokenized, bert_tokenized_ind = sentencesBertTokenize(board["content"], tok, vocab, board["name"])
            data_bert_processed.append({"name":board["name"], "content":bert_tokenized})
            data_bert_processed_ind.append(({"name":board["name"], "content":bert_tokenized_ind}))
        ##############################################
        ############### Okt Tokenizer ###############
        for board in data:
            okt_tokenized = sentencesOktTokenize(board["content"], okt, board["name"])
            okt_noun_tokenized = pickOnlyNouns(okt_tokenized)
            okt_adjv_tokenized = pickOnlyAdjsVerb(okt_tokenized)
            data_okt_noun_processed.append({"name":board["name"], "content":okt_noun_tokenized})
            data_okt_adjv_processed.append({"name":board["name"], "content":okt_adjv_tokenized})
        ##############################################
    json.dump(data_bert_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/bert_tokenized.json"), 'w'))
    json.dump(data_bert_processed_ind, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/bert_tokenized_ind.json"), 'w'))
    json.dump(data_okt_noun_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/okt_noun_tokenized.json"), 'w'))
    json.dump(data_okt_adjv_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/okt_adjv_tokenized.json"), 'w'))