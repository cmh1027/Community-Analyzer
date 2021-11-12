from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from tqdm import trange
from utility import constant
import json, os
import torch
from utility import constant
from tqdm import trange

def getMergedDocVec(formats, weight=torch.tensor([1.0, 1.0, 1.0])):
    format_vectors = []
    for format in formats:
        with open("model/d2v_"+format+".model.w2v_format") as f:
            u = f.readline()
            number = u.split(" ")[0]
            vectors = []
            for _ in trange(int(number), desc=format+" processing..."):
                vectors.append([float(i) for i in f.readline().split()[1:]])
            format_vectors.append(vectors)
    format_vectors = torch.tensor(format_vectors)
    n, p, d = format_vectors.shape
    for i in trange(n, desc="standardization..."): # standardization
        format_vectors[i] = (format_vectors[i] - torch.mean(format_vectors[i])) / torch.var(format_vectors)
    format_vectors = (format_vectors.view(n, -1) * weight[:, None]).view(n, p, d)
    merged_vector = torch.cat(format_vectors.split(1)[:], dim=2).squeeze()
    return merged_vector

if __name__ == "__main__":
    for format in constant.FORMATS:
        tokenized = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/" + format + "_tokenized.json"), 'r'))
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

        model = Doc2Vec(vector_size=constant.DOCVEC_SIZE, alpha=0.025, min_alpha=0.00025, min_count=1, dm=1, workers=4)
        vocab = tagged_data
        model.build_vocab(tagged_data)

        for epoch in trange(constant.DOC2VEC_EPOCH, desc=format+" Doc2vec training..."):
            model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
            # decrease the learning rate
            model.alpha -= 0.0002
            # fix the learning rate, no decay
            model.min_alpha = model.alpha
        modelfile = "./model/d2v_" + format + ".model"
        word2vec_file = modelfile + ".w2v_format"
        model.save(modelfile)
        model.save_word2vec_format(word2vec_file, binary=False, doctag_vec=True, word_vec=False)
    json.dump(idx2name, open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/idx2name.json"), 'w'))
    formats = constant.FORMATS
    format_vectors = []
    for format in formats:
        with open("model/d2v_"+format+".model.w2v_format") as f:
            u = f.readline()
            number = u.split(" ")[0]
            vectors = []
            for _ in trange(int(number), desc=format+" processing..."):
                vectors.append([float(i) for i in f.readline().split()[1:]])
            format_vectors.append(vectors)
    format_vectors = torch.tensor(format_vectors)
    n, p, d = format_vectors.shape
    format_vectors = (format_vectors - torch.mean(format_vectors, dim=-1).unsqueeze(-1)) / torch.sqrt(torch.var(format_vectors, dim=-1).unsqueeze(-1))
    torch.save(format_vectors, "model/d2v.w2v_format")


