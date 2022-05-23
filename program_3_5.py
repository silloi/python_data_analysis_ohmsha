# %%
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import TSNE  # scikit-learn の中の t-SNE を実行するためのライブラリのインポーt

# %%
perplexity = 30  # perplecity (基本的には 5 から 50 の間)

# %%
dataset = pd.read_csv('sample_data/iris_without_species.csv', index_col=0)
autoscaled_dataset = (dataset - dataset.mean()) / dataset.std()

# %% t-SNE
t = TSNE(perplexity=perplexity, n_components=2, init='pca', random_state=0).fit_transform(autoscaled_dataset)
t = pd.DataFrame(t, index=dataset.index, columns=['t_1', 't_2'])  # pandas の DataFrame 型に
t.to_csv('tsne_t.csv')

# %% t1 と t2 の散布図
plt.rcParams['font.size'] = 18
plt.scatter(t.iloc[:, 0], t.iloc[:, 1], c='blue')
plt.xlabel('t_1')
plt.ylabel('t_2')
plt.show()

# %%
