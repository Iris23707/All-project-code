from sklearn.base import clone
import numpy as np
import pandas as pd
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

class OOBaggingClassifier:
    def __init__(self, base_estimator, n_estimators=200):
        '''
        Parameters
        ----------
        base_estimator: a probabilistic classifier that implements the predict_proba function, such as DecisionTreeClassifier
        n_estimators: the maximum number of estimators allowed.
        '''
        self.base_estimator_ = base_estimator
        self.n_estimators = n_estimators
        self.estimators_ = []
        self.oob_errors_ = []

    def fit_basic(self, X, y, random_state=None):
        if random_state:
            np.random.seed(random_state)

        self.best_n = 0
        probs_oob = None
        oob_idxs = {}
        for i in range(self.n_estimators):
            estimator = clone(self.base_estimator_)

            bst_index = np.random.choice(range(X.shape[0]), X.shape[0], replace=True)
            oob_index = np.setdiff1d(range(X.shape[0]), bst_index)   
            oob_idxs[i] = oob_index

            bst_X = X[bst_index, :]
            bst_y = y[bst_index]
            # train on bootstrap sample
            estimator.fit(bst_X, bst_y)     
            self.estimators_.append(estimator)

            # compute oob error
            oob_predictions = []
            oob_labels = []
            oob_total = []
            # check each training data
            for k, data in enumerate(X):
                oob_estimators = []
                # find all estimators that do not use the data in training
                for j in range(i + 1):
                    if k in oob_idxs[j]:
                        oob_estimators.append(j)
                
                # calculate the oob prediction of the sample
                if len(oob_estimators) > 0:
                    oob_labels.append(y[k])
                    oob_total.append(k)
                    oob_pred = None
                    for est_id in oob_estimators:
                        pred = self.estimators_[est_id].predict_proba(np.expand_dims(data, axis=0))
                        if oob_pred is None:
                            oob_pred = pred
                        else:
                            oob_pred += pred

                    oob_predictions.append(np.argmax(oob_pred))
            # print(oob_total)
            # print(len(oob_predictions))
            oob_acc = accuracy_score(oob_labels, oob_predictions)
            oob_error = 1 - oob_acc
            self.oob_errors_.append(oob_error)

            if (self.best_n == 0) and (i >= 10 and np.mean(self.oob_errors_[i:i-5:-1]) >= np.mean(self.oob_errors_[i-5:i-10:-1])):  # replace OOB criterion with your code
                self.best_n = (i+1)

    def fit(self, X, y, random_state=None):
        if random_state:
            np.random.seed(random_state)

        self.best_n = 0

        probs_oob = None
        oob_pred_total = np.zeros((X.shape[0], 10))

        for i in range(self.n_estimators):
            estimator = clone(self.base_estimator_)

            # construct a bootstrap sample
            bst_index = np.random.choice(range(X.shape[0]), X.shape[0], replace=True)
            oob_index = np.setdiff1d(range(X.shape[0]), bst_index)
            bst_X = X[bst_index, :] #taining data features
            bst_y = y[bst_index] #training data target

            # train on bootstrap sample
            estimator.fit(bst_X, bst_y) #trained bootstrap sample
            self.estimators_.append(estimator) #list of decission tree regressor

            # compute OOB error
            oob_X = X[oob_index, :]
            # oob_y = y[oob_index]
            oob_pred = estimator.predict_proba(oob_X) #predict result of y

            for j, index in enumerate(oob_index):
                oob_pred_total[index] += oob_pred[j]

            current_oob = list(set(np.nonzero(oob_pred_total)[0]))
            # print(len(current_oob))
            current_oob_pred = np.argmax(oob_pred_total[current_oob,:], axis=1)
            oob_error = 1 - accuracy_score(y[current_oob], current_oob_pred) # replace ... with your code
            self.oob_errors_.append(oob_error)

            # save the OOB error and the new model
            self.oob_errors_.append(oob_error)
            self.estimators_.append(estimator)

            # stop early if smoothed OOB error increases (for the purpose of
            # this problem, we don't stop training when the criterion is
            # fulfilled, but simply set self.best_n to (i+1)).
            if (self.best_n == 0) and (i >= 10 and np.mean(self.oob_errors_[i:i-5:-1]) >= np.mean(self.oob_errors_[i-5:i-10:-1])):  # replace OOB criterion with your code
                self.best_n = (i+1)

    def errors(self, X, y):
        '''
        Parameters
        ----------
        X: an input array of shape (n_sample, n_features)
        y: an array of shape (n_sample,) containing the classes for the input examples

        Returns
        ------
        error_rates: an array of shape (n_estimators,), with the error_rates[i]
        being the error rate of the ensemble consisting of the first (i+1)
        models.
        '''
        error_rates = []
        # compute all the required error rates
        estimator_predictions = []

        for i, estimator in enumerate(self.estimators_):
            prob_pred = estimator.predict_proba(X)
            if i == 0:
                estimator_predictions.append(prob_pred)
            else:
                estimator_predictions.append(prob_pred + estimator_predictions[i - 1])
        
        for i in range(len(self.estimators_)):
            class_pred = np.argmax(estimator_predictions[i], axis=1)
            accuracy = accuracy_score(y, class_pred)
            error = 1 - accuracy
            error_rates.append(error)
        return error_rates



    def predict(self, X):
        '''
        Parameters
        ----------
        X: an input array of shape (n_sample, n_features)

        Returns
        ------
        y: an array of shape (n_samples,) containig the predicted classes
        '''
        probs = None
        for estimator in self.estimators_:
            p = estimator.predict_proba(X)
            if probs is None:
                probs = p
            else:
                probs += p
        return np.argmax(probs, axis=1)


# a)
digits = load_digits()
x=pd.DataFrame(digits.data,columns=digits.feature_names)
y=digits.target


random_seed = 555
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.3, random_state=random_seed)

base_estimator = DecisionTreeClassifier(random_state=random_seed)
bagging_estimator = OOBaggingClassifier(base_estimator, 100)
bagging_estimator.fit(X_train, y_train, random_seed)
print(bagging_estimator.best_n)
# print(bagging_estimator.oob_errors_)

test_error=bagging_estimator.errors(X_test,y_test)
oob_error=bagging_estimator.oob_errors_

plt.plot(range(1,201),test_error)
plt.plot(range(1,201),oob_error)
plt.legend(["test error","oob error"])
plt.xlabel("Number of models")
plt.ylabel("Error")
plt.show()

