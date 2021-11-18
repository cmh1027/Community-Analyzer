import json, os
import torch 
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from utility import constant
 
hidden_vector = torch.load('model/d2v.w2v_format')
n, p, d = hidden_vector.shape

hidden_vector = (hidden_vector.view(n, -1) * constant.WEIGHT[:, None]).view(n, p, d)
hidden_vector = torch.cat(hidden_vector.split(1)[:], dim=-1).squeeze()
hidden_vector = hidden_vector.numpy()
websites = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/idx2name.json"), 'r'))
scaler = StandardScaler()    
scaler.fit(hidden_vector)
hidden_vector = scaler.transform(hidden_vector)
pca = PCA(n_components=2)
pca.fit(hidden_vector)
reduced = pca.transform(hidden_vector)
plt.rcParams["font.family"] = 'HYGothic-Medium'
plt.rcParams["font.size"] = 8
plt.scatter(reduced[:, 0], reduced[:, 1])
plt.rc('axes', unicode_minus=False)
for i, (x, y) in enumerate(reduced):
    plt.text(x, y, websites[str(i)])
plt.show()