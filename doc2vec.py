from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import json
from utility.preprocess import sentencesTokenize
import os
website = "dcinside"
dcinside_data_tokenized = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/" + website + "_tokenized.json"), 'r'))
names = []
idx2name = {}
tagged_data = []
for data in dcinside_data_tokenized:
    name = data["name"]
    tag = len(names)
    idx2name[tag] = name
    names.append(name)
    for sentence in data["content"]:
        tagged_data.append(TaggedDocument(words=sentence, tags=[tag]))

max_epochs = 100
model = Doc2Vec(vector_size=100, alpha=0.025, min_alpha=0.00025, min_count=1, dm=1)
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha
    print("epoch : %d" % (epoch+1))


modelfile = "./model/doc2vec.model"
word2vec_file = modelfile + ".word2vec_format"
model.save("model/d2v.model")
model.save_word2vec_format(word2vec_file, binary=False, doctag_vec=True, word_vec=False)
json.dump(idx2name, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model\idx2name.json"), 'w'))



