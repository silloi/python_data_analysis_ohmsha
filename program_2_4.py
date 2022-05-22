# %%
import matplotlib.pyplot as plt
import pandas as pd

# %%
dataset = pd.read_csv('sample_data/iris_without_species.csv', index_col=0)

# %%
plt.rcParams['font.size'] = 10
pd.plotting.scatter_matrix(dataset)
plt.show()
