import numpy as np

b = np.load('/home/yiwu/inno3/CTRAS/hist/DD.npz')
print(b.shape)
print(b.files) # ['indices', 'indptr', 'format', 'shape', 'data']

