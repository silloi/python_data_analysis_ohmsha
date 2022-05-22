# %%
import matplotlib.pyplot as plt
import pandas as pd

# %%

variable_number = 0
number_of_bins = 20

dataset = pd.read_csv('sample_data/iris_without_species.csv', index_col=0)

# %% 以下でヒストグラムを描画します
plt.rcParams['font.size'] = 18
plt.hist(dataset.iloc[:, variable_number], bins=number_of_bins)
plt.xlabel(dataset.columns[variable_number])
plt.ylabel('frequency')
plt.show()
