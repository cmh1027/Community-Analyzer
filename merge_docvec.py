import torch
def getMergedDocVec(formats, weight=torch.tensor([1.0, 1.0, 1.0])):
    format_vectors = []
    for format in formats:
        with open("model/d2v_"+format+".model.w2v_format") as f:
            u = f.readline()
            number = u.split(" ")[0]
            vectors = []
            for _ in range(int(number)):
                vectors.append([float(i) for i in f.readline().split()[1:]])
            format_vectors.append(vectors)
    format_vectors = torch.tensor(format_vectors)
    n, p, d = format_vectors.shape
    for i in range(n): # standardization
        format_vectors[i] = (format_vectors[i] - torch.mean(format_vectors[i])) / torch.var(format_vectors)
    format_vectors = (format_vectors.view(n, -1) * weight[:, None]).view(n, p, d)
    merged_vector = torch.cat(format_vectors.split(1)[:], dim=2).squeeze()
    return merged_vector
if __name__ == "__main__":
    formats = ["bert", "okt_adjv", "okt_noun"]
    torch.save(getMergedDocVec(formats), "model/d2v_merged.model.w2v_format")