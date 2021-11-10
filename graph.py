import json, os
import torch 
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib as mpl
 
feature = torch.load('model/d2v_merged.model.w2v_format').numpy()
websites = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/idx2name.json"), 'r'))
scaler = StandardScaler()    
scaler.fit(feature)
feature = scaler.transform(feature)
pca = PCA(n_components=2)
pca.fit(feature)
reduced = pca.transform(feature)
plt.rcParams["font.family"] = 'HYGothic-Medium'
plt.scatter(reduced[:, 0], reduced[:, 1])
plt.rc('axes', unicode_minus=False)
for i, (x, y) in enumerate(reduced):
    plt.text(x, y, websites[str(i)])
plt.show()