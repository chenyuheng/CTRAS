import numpy as np

# b = np.load('/home/yiwu/inno3/CTRAS/hist/DD.npz')
# print(b.shape)
# print(b.files) # ['indices', 'indptr', 'format', 'shape', 'data']

distance_matrix = np.arange(16).reshape(4, 4)
print(distance_matrix)
tri = np.triu_indices(len(distance_matrix), 1)
print(tri)
distArray = distance_matrix[np.triu_indices(len(distance_matrix), 1)]
print(distArray)