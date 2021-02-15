import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from sklearn.decomposition import PCA
import warnings
warnings.simplefilter("ignore")

#2

#(a)
Hitters = pd.read_csv("D:/UQ semester2/Data 7202/Assignment 3/Hitters.csv",index_col=0)

League = LabelEncoder().fit(Hitters['League'])
Hitters['League'] = League.transform(Hitters['League'])

Division = LabelEncoder().fit(Hitters['Division'])
Hitters['Division'] = Division.transform(Hitters['Division'])

NewLeague = LabelEncoder().fit(Hitters['NewLeague'])
Hitters['NewLeague'] = NewLeague.transform(Hitters['NewLeague'])

# print(Hitters)
# print(Hitters.columns)

#(b)
y = Hitters.Salary
x = Hitters.drop(["Salary"],axis=1)
kf = KFold(n_splits=10,random_state=111)
kf.get_n_splits(x)

CV_mse = []
for train_index, test_index in kf.split(x):
    train_x, test_x = x.iloc[train_index,:],x.iloc[test_index,:]
    train_y, test_y = y.iloc[train_index], y.iloc[test_index]

    #linear regression model
    lr = LinearRegression()
    lr.fit(train_x,train_y)
    predict_y = lr.predict(test_x)

    mse = mean_squared_error(predict_y,test_y)
    CV_mse.append(round(mse,4))

mean_CV_mse = np.mean(CV_mse)
# print(CV_mse,mean_CV_mse)

#(c)
all_mse = []
for i in range(1,19):
    pca = PCA(n_components=i)
    x_pca = pca.fit_transform(x)
    x_pca = pd.DataFrame(x_pca)

    i_mse = []
    for train_index,test_index in kf.split(x_pca):
        train_x,test_x = x_pca.iloc[train_index,:],x_pca.iloc[test_index,:]
        train_y, test_y = y.iloc[train_index], y.iloc[test_index]

        lr = LinearRegression()
        lr.fit(train_x, train_y)
        predict_y = lr.predict(test_x)

        mse = mean_squared_error(predict_y, test_y)
        i_mse.append(round(mse, 4))

    mean_pca = np.mean(i_mse)
    all_mse.append(mean_pca)

# print(all_mse)

# component_number = list(range(1,19))
# fig = plt.figure(figsize=(7,7))
# plt.plot(component_number,all_mse,marker = 'o')
# x_axis = MultipleLocator(2)
# ax = plt.gca()
# ax.xaxis.set_major_locator(x_axis)
# plt.xlabel('the number of components')
# plt.ylabel('mean MSE of 10-Fold Cross-Validation')
# plt.show()

#(d)
scores = []
scores_standard_error = []
lasso = Lasso(fit_intercept=True)  # set the value of lambda
parameters = np.logspace(0,4,50)
print(parameters)

lambda_scores = {}
for parameter in parameters:
    lasso.alpha = parameter
    parameter_scores = -cross_val_score(lasso,x,y,scoring='neg_mean_squared_error',cv=10)
    mean_scores = np.mean(parameter_scores)
    lambda_scores[mean_scores] = parameter
    scores.append(mean_scores)
    scores_standard_error.append(np.std(parameter_scores))

min_score = min(scores)
print(min_score)
print(lambda_scores.get(min_score))


# plt.plot(parameters,scores)
# #plot error lines showing positive or negative standard errors of the scores
# plt.plot(parameters,np.array(scores) + np.array(scores_standard_error)/np.sqrt(len(x)),'b--')
# plt.plot(parameters,np.array(scores) - np.array(scores_standard_error)/np.sqrt(len(x)),'b--')
# plt.xlabel('lambda')
# plt.ylabel('MSE of CV')
# plt.axhline(np.max(scores),linestyle='--')
# plt.show()
