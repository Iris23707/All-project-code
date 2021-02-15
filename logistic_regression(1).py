import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_covtype
from sklearn import linear_model 

from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class LogisticRegression:
    def __init__(self):
        pass

    def fit(self, X, y, lr=0.1, momentum=0, niter=100):
        '''
        Train a multiclass logistic regression model on the given training set.

        Parameters
        ----------
        X: training examples, represented as an input array of shape (n_sample,
           n_features).
        y: labels of training examples, represented as an array of shape
           (n_sample,) containing the classes for the input examples
        lr: learning rate for gradient descent
        niter: number of gradient descent updates
        momentum: the momentum constant (see assignment task sheet for an explanation)

        Returns
        -------
        self: fitted model
        '''
        self.classes_ = np.unique(y)
        self.class2int = dict((c, i) for i, c in enumerate(self.classes_))
        y = np.array([self.class2int[c] for c in y])

        n_features = X.shape[1]
        n_classes = len(self.classes_)

        self.intercept_ = np.zeros(n_classes)
        self.coef_ = np.zeros((n_classes, n_features))


        # Implement your gradient descent training code here; uncomment the code below to do "random training"
        self.intercept_ = np.random.randn(*self.intercept_.shape)
        self.coef_ = np.random.randn(*self.coef_.shape)

        sample_number = X.shape[0]
        one_hot = np.zeros((sample_number, n_classes))
        one_hot[np.arange(sample_number), y] = 1 # Use the position of the 1 to represent the class of the corresponding number

        self.loss = []

        # According to momentum method, the next momentum value is based on the current and previous one
        # when i=0, we can't find the previous one, so I initialize the first value to 0
        previous_coef = [0, 0]
        previous_intercept = [0, 0]

        for i in range(niter):
            prob = self.predict_proba(X) # probability of forward propagation

            log_loss = one_hot * np.log(prob)
            log_loss = -1 / sample_number * np.sum(log_loss)
            self.loss.append(log_loss)

            # for each category, update its weight and bias values
            deviation_coef = -1 / sample_number * np.dot(X.T, one_hot - prob)
            deviation_intercept = -1 / sample_number * np.dot(np.ones((1, sample_number)), one_hot - prob)


            # self.coef_ -= lr * deviation_coef.T
            # self.intercept_ -= lr * deviation_intercept[0]

            if i == 0:
                self.coef_ -= lr * deviation_coef.T
                self.intercept_ -= lr * deviation_intercept[0]
                previous_coef[1] = self.coef_
                previous_intercept[1] = self.intercept_

            else:
                self.coef_ -= lr * deviation_coef.T + momentum * (previous_coef[1] - previous_coef[0])
                self.intercept_ -= lr * deviation_intercept[0] + momentum * (previous_intercept[1] - previous_intercept[0])

                previous_coef[0] = previous_coef[1]
                previous_coef[1] = self.coef_

                previous_intercept[0] = previous_intercept[1]
                previous_intercept[1] = self.intercept_



    def predict_proba(self, X):
        '''
        Predict the class distributions for given input examples.

        Parameters
        ----------
        X: input examples, represented as an input array of shape (n_sample,
           n_features).

        Returns
        -------
        y: predicted class lables, represened as an array of shape (n_sample,
           n_classes)
        '''

        # replace pass with your code
        oi_value = np.dot(X, self.coef_.T) + self.intercept_  #linear regression
        max_oi_value = np.max(oi_value, axis=1, keepdims=True)
        oi_value -= max_oi_value
        oi_value = np.exp(oi_value) #𝑒𝑜𝑦
        z = np.sum(oi_value, axis=1, keepdims=True) #∑︀𝑦′ 𝑒𝑜𝑦′
        oi_value += 1e-15 # take 15 decimal places and make it as small as possible but not equal to 0
        prob = oi_value / z
        return prob

    def predict(self, X):
        '''
        Predict the classes for given input examples.

        Parameters
        ----------
        X: input examples, represented as an input array of shape (n_sample,
           n_features).

        Returns
        -------
        y: predicted class lables, represened as an array of shape (n_sample,)
        '''

        # replace pass with your code
        probability = self.predict_proba(X)
        pred = np.argmax(probability, axis=1) + 1
        return pred

if __name__ == '__main__':
    X, y = fetch_covtype(return_X_y=True)
    X_tr, X_ts, y_tr, y_ts = train_test_split(X, y, test_size=0.3, random_state=42)

    np.random.seed(0)
    # clf = linear_model.LogisticRegression()
    clf = LogisticRegression()
    lr = 0.1
    niter = 60
    clf.fit(X_tr, y_tr, lr=lr, niter=niter)

    plt.plot(range(niter), clf.loss)
    plt.xlabel('niter')
    plt.ylabel('loss')
    plt.show()
    print(accuracy_score(y_tr, clf.predict(X_tr)))
    print(accuracy_score(y_ts, clf.predict(X_ts)))

    # clf = linear_model.LogisticRegression()
    # clf.fit(X_tr, y_tr)
    # print(accuracy_score(y_tr, clf.predict(X_tr)))
    # print(accuracy_score(y_ts, clf.predict(X_ts)))
