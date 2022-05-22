# %%
import matplotlib.pyplot as plt
import pandas as pd

# %%
variable_number_1 = 0  # 散布図における横軸の特徴量の番号
variable_number_2 = 1  # 散布図における縦軸の特徴量の番号

# %%
dataset = pd.read_csv('sample_data/iris_without_species.csv', index_col=0)

# %% 以下で散布図を描画します
plt.rcParams['font.size'] = 18
plt.scatter(dataset.iloc[:, variable_number_1], dataset.iloc[:, variable_number_2])  # 散布図の作成
plt.xlabel(dataset.columns[variable_number_1])
plt.ylabel(dataset.columns[variable_number_2])
plt.show()
