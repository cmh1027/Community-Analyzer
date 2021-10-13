import torch
def getMergedDocVec(formats, weight=[1.0, 1.0, 1.0]):
    format_vectors = []
    num_formats = len(formats)
    for format in formats:
        with open("model/d2v_"+format+".model.w2v_format") as f:
            u = f.readline()
            number = u.split(" ")[0]
            vectors = []
            for _ in range(int(number)):
                vectors.append([float(i) for i in f.readline().split()[1:]])
            format_vectors.append(vectors)
    format_vectors = torch.tensor(format_vectors)
    for i in range(num_formats): # standardization
        format_vectors[i] = (format_vectors[i] - torch.mean(format_vectors[i])) / torch.var(format_vectors)
    merged_vector = None
    for i in range(num_formats):
        if merged_vector is None:
            merged_vector = format_vectors[i] * weight[i]
        else:
            merged_vector = torch.cat((merged_vector, format_vectors[i] * weight[i]), dim=1)

    return merged_vector
if __name__ == "__main__":
    formats = ["bert", "okt_adjv", "okt_noun"]
    print(getMergedDocVec(formats))