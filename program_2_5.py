# %%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %%
dataset = pd.read_csv('sample_data/iris_without_species.csv', index_col=0)

# %%
correlation_coefficients = dataset.corr()  # 相関行列の計算
correlation_coefficients.to_csv('correlation_coefficients.csv')  # 相関行列を csv ファイルとして保存

# %% 以下で相関行列のヒートマップ（相関係数の値なし）を描画します
plt.rcParams['font.size'] = 12
sns.heatmap(correlation_coefficients, vmax=1, vmin=-1, cmap='seismic', square=True)
plt.show()

# %% 以下で相関行列のヒートマップ（相関係数の値あり）を描画します
plt.rcParams['font.size'] = 12
sns.heatmap(correlation_coefficients, vmax=1, vmin=-1, cmap='seismic', square=True, annot=True)
plt.show()
