# %%
import pandas as pd

# %%
dataset = pd.read_csv('sample_data/iris_without_species.csv', index_col=0)

# %%
basic_statistics = pd.concat(
  [dataset.min(), dataset.median(), dataset.max(), dataset.mean(), dataset.var(), dataset.std()],
  axis=1).T  # 各統計量を計算し、pd.concat() でそれらを結合
basic_statistics.index = ['min', 'median', 'max', 'mean', 'var', 'std']
basic_statistics.to_csv('basic_statistics.csv')


# %%
