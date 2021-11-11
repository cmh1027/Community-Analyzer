import json
import os
website = "dcinside"
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/bert_tokenized.json"), 'r') as json_file:
   json_data = json.load(json_file)
print(json_data)