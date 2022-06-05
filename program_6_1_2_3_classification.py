# %%
import math
import sys

# %%
import numpy as np
import pandas as pd
import sample_functions
from sklearn import metrics, svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

# %%
method_name = 'rf'  # 'knn' or 'svm' or 'rf'
add_nonlinear_terms_flag = False  # True (二乗項・交差項を追加) or False (追加しない)

# %%
number_of_test_samples = 800
fold_number = 2  # N-fold CV の N
max_number_of_k = 20  # 使用する k の最大値
svm_cs = 2 ** np.arange(-5, 11, dtype=float)
svm_gammas = 2 ** np.arange(-20, 11, dtype=float)
rf_number_of_trees = 300  # RF における決定木の数
rf_x_variables_rates = np.arange(1, 11, dtype=float) / 10  # 1 つの決定木における説明変数の数の割合の候補

# %%
if method_name != 'knn' and method_name != 'svm' and method_name != 'rf':
    sys.exit('\'{0}\' というクラス分類手法はありません。method_name を見直してください。'.format(method_name))

# %%
dataset = pd.read_csv('sample_data/unique_m.csv', index_col=-1)
dataset = dataset.sort_values('critical_temp', ascending=False).iloc[:4000, :]
y = dataset.iloc[:, 86].copy()
y[dataset.iloc[:, 86] >= 90] = 'positive'  # 転移温度 90 K 以上を高温超伝導体 (positive) とします
y[dataset.iloc[:, 86] < 90] = 'negative'
# 高温超電導体の数の調査
numbers = y.value_counts()
print('高温超電導体の数 :', numbers.iloc[1])
print('非高温超電導体の数 :', numbers.iloc[0])

# %%
x = dataset.iloc[:, :86]
x = (x.T / x.T.sum()).T
# ランダムにトレーニングデータとテストデータとに分割
# random_state に数字を与えることで、別のときに同じ数字を使えば、ランダムとはいえ同じ結果にすることができます
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=number_of_test_samples, shuffle=True,
                                                    random_state=21, stratify=y)
# 標準偏差が 0 の説明変数を削除
std_0_variable_flags = x_train.std() == 0
x_train = x_train.drop(x_train.columns[std_0_variable_flags], axis=1)
x_test = x_test.drop(x_test.columns[std_0_variable_flags], axis=1)

# %%
if add_nonlinear_terms_flag:
    x_train = pd.read_csv('sample_data/x_train_superconductor.csv', index_col=0)
    x_test = pd.read_csv('sample_data/x_test_superconductor.csv', index_col=0)
    #    x_train = sample_functions.add_nonlinear_terms(x_train)  # 説明変数の二乗項や交差項を追加
    #    x_test = sample_functions.add_nonlinear_terms(x_test)  # 説明変数の二乗項や交差項を追加
    # 標準偏差が 0 の説明変数を削除
    std_0_nonlinear_variable_flags = x_train.std() == 0
    x_train = x_train.drop(x_train.columns[std_0_nonlinear_variable_flags], axis=1)  # 標準偏差が 0 の説明変数を削除
    x_test = x_test.drop(x_test.columns[std_0_nonlinear_variable_flags], axis=1)  # 標準偏差が 0 の説明変数を削除

# %%
# オートスケーリング
autoscaled_x_train = (x_train - x_train.mean()) / x_train.std()
autoscaled_x_test = (x_test - x_train.mean()) / x_train.std()

# %%
if method_name == 'knn':
    # CV による k の最適化
    accuracy_in_cv_all = []  # 空の list の変数を作成して、成分数ごとのクロスバリデーション後の 正解率 をこの変数に追加していきます
    ks = []  # 同じく k の値をこの変数に追加していきます
    for k in range(1, max_number_of_k + 1):
        model = KNeighborsClassifier(n_neighbors=k, metric='euclidean')  # k-NN モデルの宣言
        # クロスバリデーション推定値の計算し、DataFrame型に変換
        estimated_y_in_cv = pd.DataFrame(cross_val_predict(model, autoscaled_x_train, y_train,
                                                           cv=fold_number))
        accuracy_in_cv = metrics.accuracy_score(y_train, estimated_y_in_cv)  # 正解率を計算
        print(k, accuracy_in_cv)  # k の値と r2 を表示
        accuracy_in_cv_all.append(accuracy_in_cv)  # r2 を追加
        ks.append(k)  # k の値を追加
    # k の値ごとの CV 後の正解率をプロットし、CV 後の正解率が最大のときを k の最適値に
    optimal_k = sample_functions.plot_and_selection_of_hyperparameter(ks, accuracy_in_cv_all, 'k',
                                                                      'cross-validated accuracy')
    print('\nCV で最適化された k :', optimal_k, '\n')
    # k-NN
    model = KNeighborsClassifier(n_neighbors=optimal_k, metric='euclidean')  # モデルの宣言
elif method_name == 'svm':
    # グラム行列の分散を最大化することによる γ の最適化
    optimal_svm_gamma = sample_functions.gamma_optimization_with_variance(autoscaled_x_train, svm_gammas)
    # CV による C の最適化
    model_in_cv = GridSearchCV(svm.SVC(kernel='rbf', gamma=optimal_svm_gamma),
                               {'C': svm_cs}, cv=fold_number, verbose=2)
    model_in_cv.fit(autoscaled_x_train, y_train)
    optimal_svm_c = model_in_cv.best_params_['C']
    # CV による γ の最適化
    model_in_cv = GridSearchCV(svm.SVC(kernel='rbf', C=optimal_svm_c),
                               {'gamma': svm_gammas}, cv=fold_number, verbose=2)
    model_in_cv.fit(autoscaled_x_train, y_train)
    optimal_svm_gamma = model_in_cv.best_params_['gamma']
    print('CV で最適化された C :', optimal_svm_c)
    print('CV で最適化された γ:', optimal_svm_gamma)
    # SVM
    model = svm.SVC(kernel='rbf', C=optimal_svm_c, gamma=optimal_svm_gamma)  # モデルの宣言
elif method_name == 'rf':
    # OOB (Out-Of-Bugs) による説明変数の数の割合の最適化
    accuracy_oob = []
    for index, x_variables_rate in enumerate(rf_x_variables_rates):
        print(index + 1, '/', len(rf_x_variables_rates))
        model_in_validation = RandomForestClassifier(n_estimators=rf_number_of_trees, max_features=int(
            max(math.ceil(autoscaled_x_train.shape[1] * x_variables_rate), 1)), oob_score=True)
        model_in_validation.fit(autoscaled_x_train, y_train)
        accuracy_oob.append(model_in_validation.oob_score_)
    optimal_x_variables_rate = sample_functions.plot_and_selection_of_hyperparameter(rf_x_variables_rates,
                                                                                     accuracy_oob,
                                                                                     'rate of x-variables',
                                                                                     'accuracy for OOB')
    print('\nOOB で最適化された説明変数の数の割合 :', optimal_x_variables_rate)

    # RF
    model = RandomForestClassifier(n_estimators=rf_number_of_trees,
                                   max_features=int(
                                       max(math.ceil(autoscaled_x_train.shape[1] * optimal_x_variables_rate), 1)),
                                   oob_score=True)  # RF モデルの宣言
model.fit(autoscaled_x_train, y_train)  # モデルの構築
if method_name == 'rf':
    # 説明変数の重要度
    x_importances = pd.DataFrame(model.feature_importances_, index=x_train.columns, columns=['importance'])
    x_importances.to_csv('rf_x_importances.csv')  # csv ファイルに保存。同じ名前のファイルがあるときは上書きされますので注意してください

# %%
# トレーニングデータ・テストデータの推定、混同行列の作成ト、正解率の値の表示、推定値の保存
sample_functions.estimation_and_performance_check_in_classification_train_and_test(model, autoscaled_x_train, y_train,
                                                                                   autoscaled_x_test, y_test)

# %%
