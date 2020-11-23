import numpy as np
import scipy.spatial.distance as ssd
x = np.array([[0, 2, 3, 4],
              [2, 0, 7, 8],
              [3, 7, 0, 12],
              [4, 8, 12, 0]])
y = ssd.squareform(x)
print(y)
print(type(y))