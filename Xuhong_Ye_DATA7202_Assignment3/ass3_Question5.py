import numpy as np
from sympy import *

#5

# estimated l
# generate f(x)
random_number = np.random.uniform(0,1,10000)
X = -1 * np.power(1-random_number, 1.0/3) + 1

Y = []
for i in X:
    y = 3*i + i*i - 200*cos(i)
    Y.append(y)

estimated_l = np.mean(Y)
print(estimated_l)

final_sum_square = 0
for i in Y:
    sum_square = (i - estimated_l)*(i - estimated_l)
    final_sum_square += sum_square

## 95% CI
N = 10000
sample_variance = final_sum_square / (N-1)
sample_standard_deviation  = sqrt(sample_variance/N)
upper,lower= estimated_l + 1.96 * sample_standard_deviation, estimated_l - 1.96 * sample_standard_deviation
print(sample_standard_deviation,upper,lower)

