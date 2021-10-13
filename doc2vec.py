from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from kobert.pytorch_kobert import get_pytorch_kobert_model
from tqdm import trange
from merge_docvec import getMergedDocVec
import json
import os

formats = ["bert", "okt_adjv", "okt_noun"]
for format in formats:
    tokenized = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/dcinside" + "_" + format + "_tokenized.json"), 'r'))
    names = []
    idx2name = {}
    tagged_data = []
    for data in tokenized:
        name = data["name"]
        tag = len(names)
        idx2name[tag] = name
        names.append(name)
        for sentence in data["content"]:
            tagged_data.append(TaggedDocument(words=sentence, tags=[tag]))

    max_epochs = 100
    model = Doc2Vec(vector_size=100, alpha=0.025, min_alpha=0.00025, min_count=1, dm=1)
    vocab = tagged_data
    model.build_vocab(tagged_data)

    for epoch in trange(max_epochs, desc=format+" Doc2vec training..."):
        model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha


    modelfile = "./model/d2v_" + format + ".model"
    word2vec_file = modelfile + ".w2v_format"
    model.save(modelfile)
    model.save_word2vec_format(word2vec_file, binary=False, doctag_vec=True, word_vec=False)
    json.dump(idx2name, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/idx2name" + format + ".json"), 'w'))


