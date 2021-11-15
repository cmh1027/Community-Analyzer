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
    bertmodel, vocab = get_pytorch_kobert_model()
    tokenizer = get_tokenizer()
    tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
    okt = Okt()
    for website in constant.WEBSITES_ATTIBUTES.keys():
        data = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/" + website + ".json"), 'r'))
        data_bert_processed = []
        data_bert_processed_ind = []
        data_okt_noun_processed = []
        data_okt_adjv_processed = []
        ############### Tokenize ###############
        for board in data:
            sentences = board["content"]
            content = []
            if constant.SENTENCE_NORMARLIZE is True:
                for sentence in tqdm(sentences, desc=board["name"] + " normalizing..."):
                    content.append(okt.normalize(sentence))
            else:
                content = sentences
            bert_tokenized, bert_tokenized_ind = sentencesBertTokenize(content, tok, vocab, name=board["name"])
            okt_tokenized = sentencesOktTokenize(content, okt, name=board["name"])
            okt_noun_tokenized = pickOnlyNouns(okt_tokenized)
            okt_adjv_tokenized = pickOnlyAdjsVerb(okt_tokenized)
            data_bert_processed.append({"name":board["name"], "content":bert_tokenized})
            data_bert_processed_ind.append(({"name":board["name"], "content":bert_tokenized_ind}))
            data_okt_noun_processed.append({"name":board["name"], "content":okt_noun_tokenized})
            data_okt_adjv_processed.append({"name":board["name"], "content":okt_adjv_tokenized})
        ########################################
    json.dump(data_bert_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/bert_tokenized.json"), 'w'))
    json.dump(data_bert_processed_ind, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/bert_tokenized_ind.json"), 'w'))
    json.dump(data_okt_noun_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/okt_noun_tokenized.json"), 'w'))
    json.dump(data_okt_adjv_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/okt_adjv_tokenized.json"), 'w'))