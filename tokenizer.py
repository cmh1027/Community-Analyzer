import json
import os
from utility.preprocess import sentencesBertTokenize, sentencesOktTokenize, pickOnlyNouns, pickOnlyAdjsVerb
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
from konlpy.tag import Okt
from utility import constant
import gluonnlp as nlp
from tqdm import tqdm

if __name__ == "__main__":
    okt = Okt()
    bertmodel, vocab = get_pytorch_kobert_model()
    tokenizer = get_tokenizer()
    tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
    websites = constant.WEBSITES_ATTIBUTES.keys()
    data_bert_processed = []
    data_bert_processed_ind = []
    data_okt_noun_processed = []
    data_okt_adjv_processed = []
    for website in websites:
        data = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/" + website + ".json"), 'r'))
        ############### Tokenize ###############
        bert_tokenized_each = []
        bert_tokenized_ind_each = []
        okt_noun_tokenized_each = []
        okt_adjv_tokenized_each = []
        for board in data:
            sentences = board["content"]
            sentences_splited = []
            content = []
            for sentence in tqdm(sentences, desc=board["name"] + " normalizing..."):
                if len(sentence) == 0 or len(sentence) > constant.SENTENCE_MAXLEN:
                    continue 
                content.append(okt.normalize(sentence))
            bert_tokenized, bert_tokenized_ind = sentencesBertTokenize(content, tok, vocab, name=board["name"])
            okt_tokenized = sentencesOktTokenize(content, okt, name=board["name"])
            okt_noun_tokenized = pickOnlyNouns(okt_tokenized)
            okt_adjv_tokenized = pickOnlyAdjsVerb(okt_tokenized)
            bert_tokenized_dict = {"name":board["name"], "content":bert_tokenized}
            bert_tokenized_ind_dict = {"name":board["name"], "content":bert_tokenized_ind}
            okt_noun_tokenized_dict = {"name":board["name"], "content":okt_noun_tokenized}
            okt_adjv_tokenized_dict = {"name":board["name"], "content":okt_adjv_tokenized}
            bert_tokenized_each.append(bert_tokenized_dict)
            bert_tokenized_ind_each.append(bert_tokenized_ind_dict)
            okt_noun_tokenized_each.append(okt_noun_tokenized_dict)
            okt_adjv_tokenized_each.append(okt_adjv_tokenized_dict)
        if not os.path.exists("data/{0}".format(website)):
            os.makedirs("data/{0}".format(website))
        json.dump(bert_tokenized_dict, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/{0}/bert_tokenized.json".format(website)), 'w'))
        json.dump(bert_tokenized_ind_dict, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/{0}/bert_tokenized_ind.json".format(website)), 'w'))
        json.dump(okt_noun_tokenized_dict, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/{0}/okt_noun_tokenized.json".format(website)), 'w'))
        json.dump(okt_adjv_tokenized_dict, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/{0}/okt_adjv_tokenized.json".format(website)), 'w'))
        data_bert_processed.extend(bert_tokenized_each)
        data_bert_processed_ind.extend(bert_tokenized_ind_each)
        data_okt_noun_processed.extend(okt_noun_tokenized_each)
        data_okt_adjv_processed.extend(okt_adjv_tokenized_each)
        ########################################
    json.dump(data_bert_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/bert_tokenized.json"), 'w'))
    json.dump(data_bert_processed_ind, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/bert_tokenized_ind.json"), 'w'))
    json.dump(data_okt_noun_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/okt_noun_tokenized.json"), 'w'))
    json.dump(data_okt_adjv_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/okt_adjv_tokenized.json"), 'w'))