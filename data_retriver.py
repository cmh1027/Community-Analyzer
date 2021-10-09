import json
from utility.preprocess import sentenceProprocess
import os
dcinside_data = json.load(open("data/dcinside.json"))
dcinside_data_processed = []
for data in dcinside_data:
    corpus_processed = []
    for sentence in data["content"]:
        corpus_processed.append(sentenceProprocess(sentence))
    dcinside_data_processed.append({"name":data["name"], "content":corpus_processed})
json.dump(dcinside_data_processed, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data\dcinside_procssed.json"), 'w'))
print(dcinside_data_processed)