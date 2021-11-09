import json
import os
from utility.preprocess import sentencesBertTokenize, sentencesOktTokenize, pickOnlyNouns, pickOnlyAdjsVerb
from gluonnlp.data import SentencepieceTokenizer
from kobert.utils import get_tokenizer
from konlpy.tag import Okt
import constant

if __name__ == "__main__":
    for website in constant.WEBSITES:
        tok_path = get_tokenizer()
        sp = SentencepieceTokenizer(tok_path)
        okt = Okt()
        data = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/" + website + ".json"), 'r'))
        data_bert_processed = []
        data_okt_noun_processed = []
        data_okt_adjv_processed = []
        ############### BERT Tokenizer ###############
        for board in data:
            bert_tokenized = sentencesBertTokenize(board["content"], sp, board["name"])
            data_bert_processed.append({"name":board["name"], "content":bert_tokenized})
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
    json.dump(data_okt_noun_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/okt_noun_tokenized.json"), 'w'))
    json.dump(data_okt_adjv_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/okt_adjv_tokenized.json"), 'w'))