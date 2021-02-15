import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from numpy import *
import matplotlib.pyplot as plt

#(a)
housing = fetch_california_housing()
x=pd.DataFrame(housing.data,columns=housing.feature_names)
y=housing.target

print(x.shape) #(20640,8)
#print(x.columns) #Index(['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup',
# 'Latitude', 'Longitude'],dtype='object')
#print(housing.target.shape) #(20640,)

random_seed=42
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3,random_state=random_seed)
print(x_train.shape,x_test.shape,y_train.shape,y_test.shape) #(14448, 8) (6192, 8) (14448,) (6192,)

#(b)
rfr = RandomForestRegressor(n_estimators=100,random_state=random_seed)
rfr.fit(x_train, y_train)
y_pred_train,y_pred_test=rfr.predict(x_train),rfr.predict(x_test)
train_mse=mean_squared_error(y_train,y_pred_train) #0.03698995328644075
test_mse=mean_squared_error(y_test,y_pred_test) #0.2569942567398473
print(train_mse,test_mse)

#(c)
#print(rfr.estimators_)

def get_correlation(rfr,test):
    base_learners=rfr.estimators_ #list of decission tree regressor

    base_predictions=[]
    for i in range(len(base_learners)):
        base_predictions.append(base_learners[i].predict(test))
    base_predictions=np.array(base_predictions) #shape:(110,6192)
    corr=np.corrcoef(base_predictions)

    return corr

corr=get_correlation(rfr,x_test)
print(corr) #shape:(100,100)
avg_correlation=[]
avg_correlation.append(np.mean(corr))
print(avg_correlation)

correlation=pd.DataFrame(corr)
correlation.to_csv('correlation.csv')

# average=[]
# for i in corr:
#     each_decission_tree=[]
#     for j in i:
#         if j!="1.":
#             each_decission_tree.append(j)
#         aver=mean(each_decission_tree)
#     average.append(aver)
#
# print(average)
#
# avg_correlation=[]
# avg_correlation.append(np.mean(average))
# print(avg_correlation)


#(d)
train_MSE=[]
test_MSE=[]
avg_corr=[]

for m in range(1,9):
    rfr1=RandomForestRegressor(n_estimators=100,random_state=random_seed,max_features=m)
    rfr1.fit(x_train,y_train)
    y_train_pred=rfr1.predict(x_train)
    train_MSE.append(mean_squared_error(y_train_pred,y_train))

    y_test_pred=rfr1.predict(x_test)
    test_MSE.append(mean_squared_error(y_test_pred,y_test))

    corr=get_correlation(rfr1,x_test)
    avg_corr.append(np.mean(corr))

result={"training accuracy":train_MSE,"testing accuracy":test_MSE,"average correlation":avg_corr}
result_df=pd.DataFrame(result)
result_df.to_csv("result.csv")

plt.plot(range(1,9),train_MSE)
plt.plot(range(1,9),test_MSE)
plt.plot(range(1,9),avg_corr)
plt.legend(["training MSE","test MSE","test correlation"])
plt.xlabel("Number of max features")
plt.ylabel("MSE")
# plt.show()
plt.savefig("accuracy.png")

plt.plot(range(1,9),avg_corr)
plt.xlabel("Number of max features")
plt.ylabel("Average correlation")
# plt.show()
plt.savefig("correlation.png")