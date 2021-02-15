import numpy as np

from sklearn.base import clone 
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression, RANSACRegressor, TheilSenRegressor
from sklearn.model_selection import train_test_split
from sklearn.utils import check_random_state
import matplotlib.pyplot as plt

def corrupt(X, y, outlier_ratio=0.1, random_state=None):
    random = check_random_state(random_state)

    n_samples = len(y)
    n_outliers = int(outlier_ratio*n_samples)

    W = X.copy()
    z = y.copy()

    mask = np.ones(n_samples).astype(bool)
    outlier_ids = random.choice(n_samples, n_outliers)
    mask[outlier_ids] = False

    W[~mask, 4] *= 0.1

    return W, z

class ENOLS:
    def __init__(self, n_estimators=100, sample_size='auto'):
        '''
        Parameters
        ----------
        n_estimators: number of OLS models to train
        sample_size: size of random subset used to train the OLS models, default to 'auto'
            - If 'auto': use subsets of size n_features+1 during training
            - If int: use subsets of size sample_size during training
            - If float: use subsets of size ceil(n_sample*sample_size) during training
        '''
 
        self.n_estimators = n_estimators
        self.sample_size = sample_size
    
    def fit(self, X, y, random_state=None):
        '''
        Train ENOLS on the given training set.

        Parameters
        ----------
        X: an input array of shape (n_sample, n_features)
        y: an array of shape (n_sample,) containing the values for the input examples

        Return
        ------
        self: the fitted model
        '''

        # use random instead of np.random to sample random numbers below
        random = check_random_state(random_state)

        # add all the trained OLS models to this list
        self.estimators_ = []

        # write your training code below. your code should support the
        # n_estimators and sample_size hyper-parameters described in the
        # documentation for the __init__ function
        sample_number = len(y)

        for i in range(self.n_estimators):
            if self.sample_size == "auto":
                subset_size = X.shape[1]+1
            elif isinstance(self.sample_size, int):
                subset_size = self.sample_size
            elif isinstance(self.sample_size, float):
                subset_size = np.ceil(self.sample_size*sample_number)

            subset_NO = random.choice(sample_number, subset_size) #the index of sample in subset
            lr = LinearRegression()
            lr.fit(X[subset_NO], y[subset_NO])
            self.estimators_.append(lr)

        return self
    
    def predict(self, X, method='average'):
        '''
        Parameters
        ----------
        X: an input array of shape (n_sample, n_features)
        method: 'median' or 'average', corresponding to predicting median and
            mean of the OLS models' predictions respectively.

        Returns
        -------
        y: an array of shape (n_samples,) containig the predicted values
        '''

        predicted_values = []

        for estimator in self.estimators_:
            predict_y = estimator.predict(X)
            predicted_values.append(predict_y)

        predicted_values = np.array(predicted_values) #shape(100,152)

        if method == 'average':
            predicted_values = np.mean(predicted_values, axis=0)
        elif method == 'median':
            predicted_values = np.median(predicted_values, axis=0)

        return predicted_values


def models_comparison(fig_name, n_estimators=100, method='average', sample_size='auto'):
    proportion = [0.01 * i for i in range(51)]
    OLS_MSE = []
    Theil_Sen_MSE = []
    ENOLS_MSE = []

    for p in proportion:
        W, z = corrupt(X_tr, y_tr, outlier_ratio=p, random_state=111)

        OLS_model = LinearRegression()
        OLS_model.fit(W, z)

        Theil_Sen_estimator = TheilSenRegressor()
        Theil_Sen_estimator.fit(W, z)

        ENOLS_model = ENOLS(n_estimators=n_estimators, sample_size=sample_size)
        ENOLS_model.fit(W, z, random_state=42)

        OLS_MSE.append(mean_squared_error(y_ts, OLS_model.predict(X_ts)))
        Theil_Sen_MSE.append(mean_squared_error(y_ts, Theil_Sen_estimator.predict(X_ts)))
        ENOLS_MSE.append(mean_squared_error(y_ts, ENOLS_model.predict(X_ts, method=method)))

    plt.plot(proportion, OLS_MSE, label='OLS')
    plt.plot(proportion, Theil_Sen_MSE, label='Theil-Sen')
    plt.plot(proportion, ENOLS_MSE, label='ENOLS')
    plt.legend()
    plt.savefig(fig_name)
    plt.cla()


if __name__ == '__main__':
    X, y = load_boston(return_X_y=True)
    X_tr, X_ts, y_tr, y_ts = train_test_split(X, y, test_size=0.3, random_state=111)
    W, z = corrupt(X_tr, y_tr, outlier_ratio=0.1, random_state=111)
    
    reg = LinearRegression()
    reg.fit(X_tr, y_tr)
    print(mean_squared_error(y_ts, reg.predict(X_ts)))

    reg = LinearRegression()
    reg.fit(W, z)
    print(mean_squared_error(y_ts, reg.predict(X_ts)))

    # d)
    models_comparison('Question d.png')

    # e)
    models_comparison('Question e.png', method='median')

    # f)
    models_comparison('Question f.png', n_estimators=500, method='median')

    # g)
    models_comparison('Question g.png', n_estimators=500, method='median', sample_size=42)

