import json
import os
from utility.preprocess import sentencesTokenize
from gluonnlp.data import SentencepieceTokenizer
from kobert.utils import get_tokenizer
tok_path = get_tokenizer()
sp = SentencepieceTokenizer(tok_path)
website = "dcinside"
data = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/" + website + ".json"), 'r'))
data_processed = []
for data in data:
    corpus_embedded = sentencesTokenize(data["content"], sp)
    data_processed.append({"name":data["name"], "content":corpus_embedded})
json.dump(data_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/"+ website + "_tokenized.json"), 'w'))
