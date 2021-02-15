import numpy as np
np.random.seed(12345)


#(a).
Z = np.array([8406, 2342, 8187, 8459, 4795, 3516, 4796, 10238])
Y = np.array([-1200, 2601, -2705, 1982, -1290, 351, -638, -2719])
theta_hat = np.mean(Y) / np.mean(Z)
print(np.mean(Y),np.mean(Z),theta_hat)

#(b).
B = 1000
array = np.zeros(B)

for i in range(0, B):

    # sampling with replacement len(Y) times in Y to take the corresponding Y
    y = np.random.choice(Y, size=len(Y), replace=True)

    # find the corresponding Z by the value of Y
    z = np.zeros(8)
    for j in range(0, 8):
        z[j] = Z[np.where(Y==y[j])]

    # compute the single theta
    array[i] = np.mean(y) / np.mean(z)

array_mean = np.mean(array)
array_std = np.std(array)

CI_lower = theta_hat - 1.96 * array_std
CI_upper = theta_hat + 1.96 * array_std

print("CI = (", CI_lower, ", ", CI_upper, ")")